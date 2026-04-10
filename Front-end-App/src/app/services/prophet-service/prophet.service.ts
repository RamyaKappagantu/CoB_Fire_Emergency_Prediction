import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProphetService {

  private apiUrl = 'http://127.0.0.1:5000/prophet/predict-prophet';

  constructor(private http: HttpClient) { }

  getPredictionData(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
