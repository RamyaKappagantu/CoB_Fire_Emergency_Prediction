import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ProphetService } from 'src/app/services/prophet-service/prophet.service';

@Component({
  selector: 'app-prophet-result',
  templateUrl: './prophet-result.component.html',
  styleUrls: ['./prophet-result.component.css']
})
export class ProphetResultComponent {

  predictionData: any;

  constructor(private prophetService: ProphetService) { }

  ngOnInit(): void {
    this.fetchPredictionData();
  }

  fetchPredictionData(): void {
    this.prophetService.getPredictionData().subscribe(
      data => {
        this.predictionData = {
          title: 'Prophet Model Predictions',
          nextDauid: data.next_dauid,
          nextCategory: data.next_category,
          dauidMse: data.dauid_mse,
          dauidMae: data.dauid_mae,
          dauidDirectionalAccuracy: data.dauid_directional_accuracy,
          categoryMse: data.category_mse,
          categoryMae: data.category_mae,
          categoryAccuracy: data.category_accuracy
        };
      },
      error => {
        console.error('Error fetching data:', error);
      }
    );
  }
}
