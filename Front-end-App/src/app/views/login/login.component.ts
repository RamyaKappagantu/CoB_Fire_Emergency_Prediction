import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent {
  constructor(private auth: AuthService, private router: Router, private snackBar: MatSnackBar) {}

  login(user: any): void {
    this.auth.login(user).subscribe(
      (res: any) => {
        localStorage.setItem('access_token', res.access_token);
        const decodedToken = this.auth.jwtHelper.decodeToken(res.access_token);
        this.auth.saveUser(decodedToken);
        this.router.navigate(['app']);
      },
      (err) => {
        this.snackBar.open(err.error.message, 'Close');
        console.error(err);
      }
    );
  }
}
