import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Observable } from 'rxjs';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:5000/auth';
  public jwtHelper = new JwtHelperService();
  private loggedIn = new BehaviorSubject<boolean>(this.isAuthenticated());

  constructor(private http: HttpClient) { }

  public addUser(user: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, user);
  }

  public login(user: any): Observable<any> {
    this.loggedIn.next(true);
    return this.http.post(`${this.apiUrl}/login`, user);

  }

  public isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token');
    return token !== null && !this.jwtHelper.isTokenExpired(token);
  }

  get isLoggedIn() {
    return this.loggedIn.asObservable();
  }

  public isAdmin(): boolean {
    const user = this.getUser();
    return user ? user.sub.is_admin : false;
  }

  public logout(): void {
    localStorage.removeItem('access_token');
    this.loggedIn.next(false);
    localStorage.removeItem('user');
  }

  public saveUser(user: any): void {
    localStorage.setItem('user', JSON.stringify(user));
  }

  public getUser(): any {
    return JSON.parse(localStorage.getItem('user') || '{}');
  }
}
