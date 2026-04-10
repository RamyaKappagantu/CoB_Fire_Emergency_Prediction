import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VARPredictionService {

  private apiUrl = 'http://127.0.0.1:5000/VAR_prediction/predictions';

  constructor(private http: HttpClient) { }

  getPredictions(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
