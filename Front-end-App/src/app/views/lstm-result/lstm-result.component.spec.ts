import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LSTMResultComponent } from './lstm-result.component';

describe('LSTMResultComponent', () => {
  let component: LSTMResultComponent;
  let fixture: ComponentFixture<LSTMResultComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LSTMResultComponent]
    });
    fixture = TestBed.createComponent(LSTMResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
