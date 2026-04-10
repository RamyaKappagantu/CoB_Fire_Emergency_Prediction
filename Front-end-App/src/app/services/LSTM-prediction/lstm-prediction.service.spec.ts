import { TestBed } from '@angular/core/testing';

import { LstmPredictionService } from './lstm-prediction.service';

describe('LstmPredictionService', () => {
  let service: LstmPredictionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LstmPredictionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
