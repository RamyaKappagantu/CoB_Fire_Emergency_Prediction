import { Component, EventEmitter, Output } from '@angular/core';
import { LstmPredictionService } from 'src/app/services/LSTM-prediction/lstm-prediction.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-lstm-result',
  templateUrl: './lstm-result.component.html',
  styleUrls: ['./lstm-result.component.css']
})
export class LSTMResultComponent {
  predictions: any;
  lastUpdated: string = '';
  private intervalId: any;
  private subscription: Subscription = new Subscription();
  @Output() dauidChanged = new EventEmitter<string>();
  @Output() predictionDatechanged = new EventEmitter<string>();
  predictedDauid!: string;
  prediction_date: any;

  constructor( private lstmPredictionService: LstmPredictionService) { }

  ngOnInit(): void {
    this.fetchPredictions();

    // Set an interval to fetch predictions every 15 minutes (900,000 milliseconds)
    this.intervalId = setInterval(() => {
      this.fetchPredictions();
    }, 900000);  // 15 minutes
  }

  fetchPredictions(): void {
    const currentDate = new Date().toISOString(); // Get the current date and time
    const sub = this.lstmPredictionService.getPredictions(currentDate).subscribe(
      data => {
        this.predictions = data;
        this.predictedDauid = this.predictions.da_predictions[0];
        this.prediction_date = this.predictions.Prediction_date;

        // Emit the DAUID change
        this.dauidChanged.emit(this.predictedDauid);
        this.predictionDatechanged.emit( this.prediction_date);
        // Update the last updated time
        this.lastUpdated = new Date().toLocaleString();
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
