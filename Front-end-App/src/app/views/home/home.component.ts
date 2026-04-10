import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth/auth.service';
import { FileUploadService } from 'src/app/services/file-upload/file-upload.service';

@Component({
  selector: 'app-root',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  dauid!: string;
  predictionDate!: string;
  user: any;

  constructor(private fileUploadService: FileUploadService,public authService: AuthService, private router: Router) { 
    this.user = this.authService.getUser();
    console.log(this.user)
  }
  
  onDauidChanged(newDauid: string) {
    this.dauid = newDauid;
  }

  onPredictionDateChanged(newPredictionDate: string){
    this.predictionDate = newPredictionDate;
  }

  triggerFileInput() {
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    fileInput.click();
  }

  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.uploadFile(file);
    }
  }

  uploadFile(file: File) {
    this.fileUploadService.uploadFile(file).subscribe(
      response => {
        console.log('File successfully uploaded', response);
      },
      error => {
        console.error('Error uploading file', error);
      }
    );
  }

}
