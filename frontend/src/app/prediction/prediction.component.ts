import { Component, OnInit,Input } from '@angular/core';
import { GetdataService } from '../getdata.service';
import * as CanvasJS from '../../assets/canvasjs.min';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'ngbd-modal-content',
  template: `
    <div class="modal-header">
      <h1 class="modal-title"><b>Here comes result!</b></h1>
    </div>
    <div class="modal-body">
      <div *ngIf="predict==1 ;else elseBlock">
        <h2 style="color:red;"><b>Crap!</b></h2 ><h2 > Looks like a large probability indicates you have Heart Disease! Please go see a doctor <b>ASAP!</b> </h2 >
        <img src="assets/images/sad.png">
      </div>
          <ng-template #elseBlock><h2 style="color:green;"><b>congratulations!</b></h2 ><h2>It seems you do not have heart disease.</h2 >
            <img class="w-100" src="assets/images/happy.jpg">
          </ng-template>
     </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-outline-dark" (click)="activeModal.close('Close click')">Close</button>
    </div>
  `
})
export class NgbdModalContent {
  @Input() predict;
  constructor(public activeModal: NgbActiveModal) {
  }
}

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})

export class PredictionComponent implements OnInit {
  form: FormGroup;
  submitted = false;
  model_choose = true;
  predict: number;
  pain_type_select = [
    "1 - typical angin",
    "2 - atypical angina",
    "3 - non-anginal pain",
    "4 - asymptomatic"
  ]
  electrocardiographic_select = [
    "0 - normal",
    "1 - having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)",
    "2 - showing probable or definite left ventricular hypertrophy by Estes’ criteria"
  ]
  thal_select = [
    "3 - normal",
    "6 - fixed defect",
    "7 - reversable defect"
  ]


  constructor(private getdataservice: GetdataService,
              private formBuilder: FormBuilder,
              private router: Router,
              private modalService: NgbModal) {
    this.form = this.createFormGroup();
  }

  get f() {
    return this.form.controls;
  }

  ngOnInit() {
  }

  createFormGroup() {
    return this.formBuilder.group({
      age: '',
      sex: '',
      pain_type: '',
      blood_pressure: '',
      cholestoral: '',
      blood_sugar: '',
      electrocardiographic: '',
      heart_rate: '',
      angina: '',
      oldpeak: '',
      ST_segment: '',
      vessels: ['', Validators.compose([Validators.min(0), Validators.max(3)])],
      thal: ''
    })
  }

  toggleDataSeries(e) {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
      e.dataSeries.visible = false;
    } else {
      e.dataSeries.visible = true;
    }
    e.chart.render();
  }

  showdata(data, methed) {
    let train_score = [];
    let valid_score = [];
    for (let i = 20; i <= 260; i += 20) {
      train_score.push({ x: i, y: data["train_score"][i]*100 });
      valid_score.push({ x: i, y: data["valid_score"][i]*100 });
    }
    var chart = new CanvasJS.Chart("chartContainer", {
      animationEnabled: true,
      exportEnabled: true,
      title: {
        text: `Learning Curve with ${methed}`
      },
      axisY: {
        title: "Accuracy",
        suffix: "%"
      },
      axisX: {
        title: "Number of input samples"
      },
      toolTip: {
        shared: true
      },
      legend: {
        cursor: "pointer",
        itemclick: this.toggleDataSeries
      },
      data: [{
        type: "spline",
        name: "train score",
        showInLegend: true,
        dataPoints: train_score
      },
      {
        type: "spline",
        name: "valid score",
        showInLegend: true,
        dataPoints: valid_score
      }]
    });

    chart.render();
  }

  drawLogit() {
    this.getdataservice.getcurve("logit").subscribe(
      graphdata => {
        this.showdata(graphdata, 'logistic regression')
      }
    );
  }

  drawStack() {
    this.getdataservice.getcurve("stack").subscribe(
      graphdata => {
        this.showdata(graphdata, 'stacked methods')
      }
    );
  }
  open() {
    const modalRef = this.modalService.open(NgbdModalContent);
    modalRef.componentInstance.predict = this.predict;
  }

  onSubmit() {
    this.submitted = true;
    if (this.form.invalid) {
      return
    }
    let temp = [this.form.value.age,
    this.form.value.sex,
    this.form.value.pain_type.slice(0, 1),
    this.form.value.blood_pressure,
    this.form.value.cholestoral,
    this.form.value.blood_sugar,
    this.form.value.electrocardiographic.slice(0, 1),
    this.form.value.heart_rate,
    this.form.value.angina,
    this.form.value.oldpeak,
    this.form.value.ST_segment,
    this.form.value.vessels,
    this.form.value.thal.slice(0, 1)];
    for (let i = 0; i < temp.length;i++) {
      if (temp[i] == null || temp[i]== ''){
        temp[i] = '%3F';
      }
    }
    if (this.model_choose) {
      this.getdataservice.predict("logit",
        temp[0],
        temp[1],
        temp[2],
        temp[3],
        temp[4],
        temp[5],
        temp[6],
        temp[7],
        temp[8],
        temp[9],
        temp[10],
        temp[11],
        temp[12]).subscribe
        (
          data=>{
            this.predict = data.target;
            this.open()
          }
      );
      this.drawLogit();
    }
    else {
      this.getdataservice.predict("stack",
        temp[0],
        temp[1],
        temp[2],
        temp[3],
        temp[4],
        temp[5],
        temp[6],
        temp[7],
        temp[8],
        temp[9],
        temp[10],
        temp[11],
        temp[12]).subscribe
        (
        data => {
          this.predict = data.target;
          this.open()
        }
      );
      this.drawStack();
    }
  }
  setLogit() {
    this.model_choose = true;
  }
  setStack() {
    this.model_choose = false;
  }
}
