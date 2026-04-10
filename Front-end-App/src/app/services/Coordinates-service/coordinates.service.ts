import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CoordinatesService {
  private apiUrl = 'http://127.0.0.1:5000/coordinates/get-all-das-coordinates';

  constructor(private http: HttpClient) {}

  getAllCoordinates(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
