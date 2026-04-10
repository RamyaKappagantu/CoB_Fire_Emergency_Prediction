import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html'
})
export class RegisterComponent {
  constructor(private auth: AuthService, private router: Router, private snackBar: MatSnackBar) {}

  addUser(user: any): void {
     this.auth.addUser(user).subscribe(
      (res: any) => {
        this.snackBar.open('User created successfully', 'Close');
        this.router.navigate(['home']);
      },
      (err) => {
        this.snackBar.open(err.error.message, 'Close');
        console.error(err);
      }
    );
  }
}
