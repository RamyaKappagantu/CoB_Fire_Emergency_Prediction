import { TestBed } from '@angular/core/testing';

import { ProphetService } from './prophet.service';

describe('ProphetService', () => {
  let service: ProphetService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProphetService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
