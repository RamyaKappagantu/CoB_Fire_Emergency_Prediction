import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { LstmPredictionService } from 'src/app/services/LSTM-prediction/lstm-prediction.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-date-picker',
  templateUrl: './date-picker.component.html',
  styleUrls: ['./date-picker.component.css']
})
export class DatePickerComponent implements OnInit {
  @Output() dauidChanged = new EventEmitter<string>();
  @Output() predictionDatechanged = new EventEmitter<string>();
  predictions: any;
  predictedDauid: string = '';
  lastUpdated: string = '';
  selectedDate: string = ''; 
  subscription: Subscription = new Subscription();
  prediction_date: any;

  constructor(private lstmPredictionService: LstmPredictionService) {}

  ngOnInit(): void {
    this.selectedDate = new Date().toISOString(); // Initialize with current date
  }

  onDateChange(event: any): void {
    this.selectedDate = event.value.toISOString(); // Update the selected date
  }

  fetchPredictions(): void {
    const sub = this.lstmPredictionService.getPredictions(this.selectedDate).subscribe(
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
    this.subscription.unsubscribe();
  }
}
