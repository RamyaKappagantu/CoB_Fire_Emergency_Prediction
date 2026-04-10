import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LstmPredictionService {

  private apiUrl = 'http://127.0.0.1:5000/lstm_prediction/predictions';

  constructor(private http: HttpClient) { }

  getPredictions(date: string): Observable<any> {
    const params = { date };
    return this.http.get<any>(this.apiUrl, { params });
  }
}
