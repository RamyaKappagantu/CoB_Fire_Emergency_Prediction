import { Component } from '@angular/core';
import { VARPredictionService } from 'src/app/services/VAR-prediction/VAR-prediction.service';
import { Subscription } from 'rxjs';


@Component({
  selector: 'app-var-result',
  templateUrl: './var-result.component.html',
  styleUrls: ['./var-result.component.css']
})
export class VARResultComponent {
  predictions: any;
  private intervalId: any;
  private subscription: Subscription = new Subscription();

  constructor( private VARPredictionService: VARPredictionService) { }

  ngOnInit(): void {
    this.fetchPredictions();

    // Set an interval to fetch predictions every 15 minutes (900,000 milliseconds)
    this.intervalId = setInterval(() => {
      this.fetchPredictions();
    }, 900000);  // 15 minutes
  }

  fetchPredictions(): void {
    const sub = this.VARPredictionService.getPredictions().subscribe(
      data => {
        this.predictions = data;
      },
      error => {
        console.error('Failed to fetch predictions:', error);
      }
    );
    this.subscription.add(sub);
  }

  ngOnDestroy(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    this.subscription.unsubscribe();
  }
}
