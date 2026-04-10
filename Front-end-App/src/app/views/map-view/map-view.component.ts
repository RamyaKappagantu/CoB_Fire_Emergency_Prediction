import { Component, Input, OnInit, SimpleChanges } from '@angular/core';
import * as L from 'leaflet';
import { Map } from 'leaflet';
import 'proj4leaflet';
import * as JSZip from 'jszip';
import * as shapefile from 'shapefile';
import shp from 'shpjs';
import { HttpClient } from '@angular/common/http';
import { FeatureCollection, Feature, Geometry, GeoJsonProperties } from 'geojson';
import * as proj4 from 'proj4';
import * as turf from '@turf/turf';
import { point } from '@turf/helpers';
import { toWgs84 } from '@turf/projection';
import {CoordinatesService} from 'src/app/services/Coordinates-service/coordinates.service';


@Component({
  selector: 'app-map-view',
  templateUrl: './map-view.component.html',
  styleUrls: ['./map-view.component.css']
})
export class MapViewComponent implements OnInit{
  private map!: L.Map;
  @Input() daId!: string;
  @Input() newPredictionDate!: string;
  private allDAs: any[] = [];
  private dataLoaded = false;
  private highlightedPolygon: L.Polygon | null = null;
  private highlightedMarker: L.Marker | null = null;

  constructor(private coordinatesService: CoordinatesService) {}

  ngOnInit() {
    this.initMap();
    this.loadAllCoordinates();
  }

  ngOnChanges(changes: SimpleChanges): void  {
    if (changes['daId'] && this.daId) {
      if (this.dataLoaded) {
        this.highlightNextEmergencyDA(this.daId);
      } else {
        console.log("waiting for dtaloaded");
        // Wait for data to be loaded before highlighting
        this.waitForDataLoad().then(() => {
          this.highlightNextEmergencyDA(this.daId);
        });
      }
    }
  }

  private initMap(): void {
    this.map = L.map('map').setView([44.36962587578148, -79.65347124895777], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 35,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.map);

    this.addLegend();
  }

  private loadAllCoordinates(): void {
    this.coordinatesService.getAllCoordinates().subscribe(response => {
      this.allDAs = response;
      this.dataLoaded = true; 
      this.displayAllDAs();
    }, error => {
      console.error('Error loading all DA coordinates:', error);
    });
  }

  private displayAllDAs(): void {
    this.allDAs.forEach(da => {
      const severityScore = parseInt(da.severity_score.Composite_Severity_Score, 10);
      if (!isNaN(severityScore)) {
        this.addPolygon(da.polygon_coords, severityScore, da.DAUID === this.daId);
      } else {
        // Handle the case where severity score is not a valid number
        console.error(`Invalid severity score for DAUID: ${da.DAUID}`);
      }
    });
  }

  private highlightNextEmergencyDA(daId: string): void {
    // Remove the previous highlight and marker, if any
    if (this.highlightedPolygon) {
      this.map.removeLayer(this.highlightedPolygon);
      this.highlightedPolygon = null;
    }
    if (this.highlightedMarker) {
      this.map.removeLayer(this.highlightedMarker);
      this.highlightedMarker = null;
    }


    this.allDAs.forEach(da => {
      if (da.DAUID == daId) {
        const severityScore = parseInt(da.severity_score.Composite_Severity_Score, 10);
        if (!isNaN(severityScore)) {
          this.highlightedPolygon = this.addPolygon(da.polygon_coords, severityScore, true);
          this.highlightedMarker = this.addMarker(da.center);
        } else {
          // Handle the case where severity score is not a valid number
          console.error(`Invalid severity score for DAUID: ${da.DAUID}`);
        }      
      }
    });
  }

  private addPolygon(coords: any[], severityScore: number, highlight: boolean): L.Polygon {
    const latLngs = coords.map(coord => [coord.lat, coord.lng]);
    const polygon = L.polygon(latLngs, {
      color: highlight ? 'purple' : this.getSeverityColor(severityScore),
      weight: highlight ? 5 : 3,
      opacity: 1,
      fillOpacity: 0.5
    }).addTo(this.map);

    if (highlight) {
      this.map.fitBounds(polygon.getBounds());
    }

    // Return the created polygon to be stored in highlightedPolygon
    return polygon;
  }

  private addMarker(center: any): L.Marker {
    console.log("addMArker");
    const marker = L.marker([center.lat, center.lng], {
      icon: L.icon({
        iconUrl: 'assets/map-marker.webp',
        iconSize: [25, 41], // Size of the icon
        iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
        popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
        shadowSize: [41, 41] // Optional: Size of the shadow
      })
    }).addTo(this.map).bindPopup(`
      <div>
        <strong>Next Emergency DAUID:</strong> ${this.daId}<br>
        <strong>Prediction Date:</strong> ${this.newPredictionDate}
      </div>
    `).openPopup();

    return marker
  }

  private getSeverityColor(score: number): string {
    switch (score) {
      case 5: return '#6a1b9a'; // dark purple
      case 4: return '#9c27b0'; // purple
      case 3: return '#f44336'; // red
      case 2: return '#ff9800'; // orange
      case 1: return '#ffeb3b'; // yellow
      default: return '#d3d3d3'; // light grey
    }
  }

  private waitForDataLoad(): Promise<void> {
    return new Promise((resolve) => {
      const checkDataLoaded = () => {
        console.log('Checking if data is loaded...');
        if (this.dataLoaded) {
          console.log('Data loaded!');
          resolve();
        } else {
          setTimeout(checkDataLoaded, 100); // Check every 100 milliseconds
        }
      };
      checkDataLoaded();
    });
  }

  private addLegend(): void {
    const legend = new (L.Control.extend({
      options: { position: 'bottomleft' }
    }))();

    legend.onAdd = (map: L.Map) => {
      const div = L.DomUtil.create('div', 'info legend');
      const grades = [1, 2, 3, 4, 5];
      const colors = [
        '#ffeb3b', // yellow
        '#ff9800', // orange
        '#f44336', // red
        '#9c27b0', // purple
        '#6a1b9a'  // dark purple
      ];

      div.innerHTML += '<strong>Severity Score</strong><br>';
      for (let i = 0; i < grades.length; i++) {
        div.innerHTML +=
          '<i style="background:' + colors[i] + '; width: 18px; height: 18px; display: inline-block; margin-right: 8px;"></i> ' +
          grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
      }


      return div;
    };

    legend.addTo(this.map);
  }
}