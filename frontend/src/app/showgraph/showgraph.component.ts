import { Component, OnInit } from '@angular/core';
import { GetdataService } from '../getdata.service';
import * as CanvasJS from '../../assets/canvasjs.min';
@Component({
  selector: 'app-showgraph',
  templateUrl: './showgraph.component.html',
  styleUrls: ['./showgraph.component.css']
})
export class ShowgraphComponent implements OnInit {
  d: object;
  type: string;
  totaldatanumber: number;

  constructor(
    private getdataservice:GetdataService,

  ) {}

  getRandomColor(n:number) {
    var palette = ['#003366', '#cc0000', '#9966ff', '#009900', '#cc99ff', '#00ccff', '#663300', '#993333', '#ffccff', '#6699ff', '#003300', '#666699','#ff9900'];
    return palette[n];
}

  ngOnInit() {

  }
  pain_type() {
    this.type = 'pain_type';
    this.pain_type_age();
    this.pain_type_sex();
  }


  electrocardiographic() {
    this.type = 'electrocardiographic';
    this.electrocardiographic_age();
    this.electrocardiographic_sex();
  }

  blood_sugar() {
    this.type = 'blood_sugar';
    this.blood_sugar_age();
    this.blood_sugar_sex();
  }

  angina() {
    this.type = 'angina';
    this.angina_age();
    this.angina_sex();
  }

  Vessels() {
    this.type = 'Vessels';
    this.Vessels_age();
    this.Vessels_sex();
  }

  Thalassemia() {
    this.type = 'Vessels';
    this.Thalassemia_age();
    this.Thalassemia_sex();
  }

  Thalassemia_sex() {
    let dataPoints = [];
    this.getdataservice.getdata(13).subscribe(
      data => {
        dataPoints.push({
          type: "bar",
          showInLegend: true,
          name: 'Female',
          color: '#ff0000',
          dataPoints: [
            { y: 0, label: "normal" },
            { y: 0, label: " fixed defect" },
            { y: 0, label: " reversable defect" }]
        });
        dataPoints.push({
          type: "bar",
          showInLegend: true,
          name: 'Male',
          color: '#000000',
          dataPoints: [
            { y: 0, label: "normal" },
            { y: 0, label: " fixed defect" },
            { y: 0, label: " reversable defect" }]
        });

        let male_number = 0
        let female_number = 0
        for (let d of data.data) {
          if (d.sex == 0) {
            female_number++;
          }
          else {
            male_number++;
          }
         if (d.value == 3.0) {
           dataPoints[Math.floor(d.sex)].dataPoints[0].y++;
          }
          else if (d.value == 6.0) {
           dataPoints[Math.floor(d.sex)].dataPoints[1].y++;
          }
          else {
           dataPoints[Math.floor(d.sex)].dataPoints[2].y++;
          }
        }
        for (let i = 0; i < 3; i++) {
          dataPoints[0].dataPoints[i].y = dataPoints[0].dataPoints[i].y / female_number * 100
          dataPoints[1].dataPoints[i].y = dataPoints[1].dataPoints[i].y / male_number * 100
        }
        this.barchat(dataPoints, 'Thalassemia vs. Sex', 'Percentage of Population in Sex', 'chartContainer_sex');
      });
  }

  Thalassemia_age() {
    let dataPoints = [];
    this.getdataservice.getdata(13).subscribe(
      data => {
        let max = 0
        for (let d of data.data) {
          if (d.age > max) {
            max = d.age
          }
        }
        let group = Math.ceil(max / 10);
        let group_total = [];
        for (let i = 0; i < group; i++) {
          dataPoints.push({
            type: "bar",
            showInLegend: true,
            name: `${i * 10} to ${(i + 1) * 10} years old`,
            color: this.getRandomColor(i),
            dataPoints: [
              { y: 0, label: "normal" },
              { y: 0, label: " fixed defect" },
              { y: 0, label: " reversable defect" }]
          });
          group_total.push(0);
        }
        for (let d of data.data) {
          if (d.value == 3.0) {
            dataPoints[Math.floor(d.age / 10)].dataPoints[0].y++;
          }
          else if (d.value == 6.0) {
            dataPoints[Math.floor(d.age / 10)].dataPoints[1].y++;
          }
          else {
            dataPoints[Math.floor(d.age / 10)].dataPoints[2].y++;
          }
          
          group_total[Math.floor(d.age / 10)]++;
        }
        for (let i = 0; i < group; i++) {
          for (let d of dataPoints[i].dataPoints) {
            d.y = d.y / group_total[i] * 100;
          }
        }
        this.barchat(dataPoints, 'Thalassemia vs. Age', 'Percentage of Population in Each Group', 'chartContainer_age');
      });
  }

  Vessels_sex() {
    let dataPoints = [];
    this.getdataservice.getdata(12).subscribe(
      data => {
        dataPoints.push({
          type: "bar",
          showInLegend: true,
          name: 'Female',
          color: '#ff0000',
          dataPoints: [
            { y: 0, label: "0.0" },
            { y: 0, label: "1.0" },
            { y: 0, label: "2.0" },
            { y: 0, label: "3.0" }]
        });
        dataPoints.push({
          type: "bar",
          showInLegend: true,
          name: 'Male',
          color: '#000000',
          dataPoints: [
            { y: 0, label: "0.0" },
            { y: 0, label: "1.0" },
            { y: 0, label: "2.0" },
            { y: 0, label: "3.0" }]
        });

        let male_number = 0
        let female_number = 0
        for (let d of data.data) {
          if (d.sex == 0) {
            female_number++;
          }
          else {
            male_number++;
          }
          dataPoints[Math.floor(d.sex)].dataPoints[(Math.floor(d.value ))].y++;
        }
        for (let i = 0; i < 4; i++) {
          dataPoints[0].dataPoints[i].y = dataPoints[0].dataPoints[i].y / female_number * 100
          dataPoints[1].dataPoints[i].y = dataPoints[1].dataPoints[i].y / male_number * 100
        }
        this.barchat(dataPoints, 'Number of Major Vessels vs. Sex', 'Percentage of Population in Sex', 'chartContainer_sex');
      });
  }

  Vessels_age() {
    let dataPoints = [];
    this.getdataservice.getdata(12).subscribe(
      data => {
        let max = 0
        for (let d of data.data) {
          if (d.age > max) {
            max = d.age
          }
        }
        let group = Math.ceil(max / 10);
        let group_total = [];
        for (let i = 0; i < group; i++) {
          dataPoints.push({
            type: "bar",
            showInLegend: true,
            name: `${i * 10} to ${(i + 1) * 10} years old`,
            color: this.getRandomColor(i),
            dataPoints: [
              { y: 0, label: "0.0" },
              { y: 0, label: "1.0" },
              { y: 0, label: "2.0" },
              { y: 0, label: "3.0" }]
          });
          group_total.push(0);
        }
        for (let d of data.data) {
          dataPoints[Math.floor(d.age / 10)].dataPoints[(Math.floor(d.value))].y++;
          group_total[Math.floor(d.age / 10)]++;
        }
        for (let i = 0; i < group; i++) {
          for (let d of dataPoints[i].dataPoints) {
            d.y = d.y / group_total[i] * 100;
          }
        }
        this.barchat(dataPoints, 'Number of Major Vessels vs. Age', 'Percentage of Population in Each Group', 'chartContainer_age');
      });
  }


  angina_age() {
    this.getdataservice.getdata(9).subscribe(
      data => {
        let max = 0
        for (let d of data.data) {
          if (d.age > max) {
            max = d.age
          }
        }
        let group = Math.ceil(max / 10);
        let dataPoints_false = [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "##0.00\"%\"",
          indexLabel: "{label} {y}",
          dataPoints: [],
        }]

        let dataPoints_true = [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "##0.00\"%\"",
          indexLabel: "{label} {y}",
          dataPoints: []
        }]
        for (let i = 0; i < group; i++) {
          dataPoints_false[0].dataPoints.push({ y: 0, label: `${i * 10} to ${(i + 1) * 10}` });
          dataPoints_true[0].dataPoints.push({ y: 0, label: `${i * 10} to ${(i + 1) * 10}` })
        }
        let totalmale = 0;
        let totalfemale = 0;
        for (let d of data.data) {
          if (d.value == 1.0) {
            totalmale++;
            dataPoints_true[0].dataPoints[Math.floor(d.age / 10)].y++;
          }
          else {
            totalfemale++;
            dataPoints_false[0].dataPoints[Math.floor(d.age / 10)].y++;
          }
        }
        for (let i = 0; i < group; i++) {
          dataPoints_true[0].dataPoints[i].y = dataPoints_true[0].dataPoints[i].y / totalmale * 100;
          dataPoints_false[0].dataPoints[i].y = dataPoints_true[0].dataPoints[i].y / totalmale * 100;
        }
        this.pie_chart('chartContainer_pie_true_age', 'Angina True', dataPoints_true);
        this.pie_chart('chartContainer_pie_false_age', 'Angina False', dataPoints_false);
      }
    );
  }


  angina_sex() {
    this.getdataservice.getdata(9).subscribe(
      data => {

        let dataPoints_male = [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "##0.00\"%\"",
          indexLabel: "{label} {y}",
          dataPoints: [],
        }]

        let dataPoints_female = [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "##0.00\"%\"",
          indexLabel: "{label} {y}",
          dataPoints: []
        }]
        dataPoints_male[0].dataPoints.push({ y: 0, label: 'False' });
        dataPoints_male[0].dataPoints.push({ y: 0, label: 'True' });

        dataPoints_female[0].dataPoints.push({ y: 0, label: `False` })
        dataPoints_female[0].dataPoints.push({ y: 0, label: `True` })
        let totalmale = 0;
        let totalfemale = 0;

        for (let d of data.data) {
          if (d.sex == 1.0) {
            totalmale++;
            dataPoints_male[0].dataPoints[Math.floor(d.value)].y++;
          }
          else {
            totalfemale++;
            dataPoints_female[0].dataPoints[Math.floor(d.value)].y++;
          }
        }
        dataPoints_male[0].dataPoints[0].y = dataPoints_male[0].dataPoints[0].y * 100 / totalmale;
        dataPoints_male[0].dataPoints[1].y = dataPoints_male[0].dataPoints[1].y * 100 / totalmale;

        dataPoints_female[0].dataPoints[0].y = dataPoints_female[0].dataPoints[0].y * 100 / totalfemale;
        dataPoints_female[0].dataPoints[1].y = dataPoints_female[0].dataPoints[1].y * 100 / totalfemale;
        console.log(dataPoints_female);
        console.log(dataPoints_male);
        this.pie_chart('chartContainer_pie_male', 'Angina Male', dataPoints_male);
        this.pie_chart('chartContainer_pie_female', 'Angina Female', dataPoints_female);
      }
    );
  }
  oldpeak() {
    this.type = 'oldpeak';
    let dataPoints_male = [];
    let dataPoints_female = [];
    var count: { [id: string]: { x: number, y: number, z: number, name: string } } = {};
    this.getdataservice.getdata(10).subscribe(
      data => {
        for (let d of data.data) {
          if (count[`${d.age} ${d.value} ${d.sex}`] == undefined) {
            if (d.sex == 0.0) {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'female' };
            }
            else {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'male' };
            }
          }
          else {
            count[`${d.age} ${d.value} ${d.sex}`].z++;
          }
        }

        for (var key in count) {
          if (count[key].name == 'female') {
            dataPoints_female.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
          else {
            dataPoints_male.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
        }
        this.continous_bubble_data(dataPoints_male, dataPoints_female, "ST depression induced by exercise relative to rest vs. Age in Different Sex", "Age", "Oldpeak",
          "<b>Male</b><br/>Age: {x} yrs<br/> Oldpeak: {y}<br/> Population: {z}",
          "<b>Female</b><br/>Age: {x} yrs<br/> Oldpeak: {y}<br/> Population: {z}",
          50, -6, 10);
      });
  }
  ST_segment() {
    this.type = 'ST_segment';
    let dataPoints_male = [];
    let dataPoints_female = [];
    var count: { [id: string]: { x: number, y: number, z: number, name: string } } = {};
    this.getdataservice.getdata(11).subscribe(
      data => {
        for (let d of data.data) {
          if (count[`${d.age} ${d.value} ${d.sex}`] == undefined) {
            if (d.sex == 0.0) {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'female' };
            }
            else {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'male' };
            }
          }
          else {
            count[`${d.age} ${d.value} ${d.sex}`].z++;
          }
        }

        for (var key in count) {
          if (count[key].name == 'female') {
            dataPoints_female.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
          else {
            dataPoints_male.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
        }
        this.continous_bubble_data(dataPoints_male, dataPoints_female, "The Slope of The Peak Exercise ST Segment vs. Age in Different Sex", "Age", "ST Segment",
          "<b>Male</b><br/>Age: {x} yrs<br/> ST Segment: {y}<br/> Population: {z}",
          "<b>Female</b><br/>Age: {x} yrs<br/> ST Segment: {y}<br/> Population: {z}",
          50, -2, 40);
      });
  }

  heart_rate() {
    this.type = 'heart_rate';
    let dataPoints_male = [];
    let dataPoints_female = [];
    var count: { [id: string]: { x: number, y: number, z: number, name: string } } = {};
    this.getdataservice.getdata(8).subscribe(
      data => {
        for (let d of data.data) {
          if (count[`${d.age} ${d.value} ${d.sex}`] == undefined) {
            if (d.sex == 0.0) {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'female' };
            }
            else {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'male' };
            }
          }
          else {
            count[`${d.age} ${d.value} ${d.sex}`].z++;
          }
        }

        for (var key in count) {
          if (count[key].name == 'female') {
            dataPoints_female.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
          else {
            dataPoints_male.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
        }
        this.continous_bubble_data(dataPoints_male, dataPoints_female, "Maximum Heart Rate Achieved vs. Age in Different Sex", "Age", "Heart Rate",
          "<b>Male</b><br/>Age: {x} yrs<br/> Heart Rate: {y}<br/> Population: {z}",
          "<b>Female</b><br/>Age: {x} yrs<br/> Heart Rate: {y}<br/> Population: {z}",
          40, 200, 20);
      });
  }

  serum_cholestoral() {
    this.type = 'serum_cholestoral';
    let dataPoints_male = [];
    let dataPoints_female = [];
    var count: { [id: string]: { x: number, y: number, z: number, name: string } } = {};
    this.getdataservice.getdata(5).subscribe(
      data => {
        for (let d of data.data) {
          if (count[`${d.age} ${d.value} ${d.sex}`] == undefined) {
            if (d.sex == 0.0) {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'female' };
            }
            else {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'male' };
            }
          }
          else {
            count[`${d.age} ${d.value} ${d.sex}`].z++;
          }
        }

        for (var key in count) {
          if (count[key].name == 'female') {
            dataPoints_female.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
          else {
            dataPoints_male.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
        }
        this.continous_bubble_data(dataPoints_male, dataPoints_female, "Serum Cholestoral vs. Age in Different Sex", "Age", "Serum Cholestoral",
          "<b>Male</b><br/>Age: {x} yrs<br/> Blood Pressure: {y}<br/> Population: {z}",
          "<b>Female</b><br/>Age: {x} yrs<br/> Blood Pressure: {y}<br/> Population: {z}",
          40, 200, 20);
      });
  }

  continous_bubble_data(dataPoints_male, dataPoints_female, title, axisX_title, axisY, toolTipContent_male, toolTipContent_female,fake_x,fake_y,fake_z) {
    var chart = new CanvasJS.Chart("continous_bubble_data", {
      animationEnabled: true,
      title: {
        text: title
      },
      axisX: {
        title: axisX_title
      },
      axisY: {
        title: axisY
      },
      legend: {
        horizontalAlign: "left"
      },
      data: [
        {
          type: "bubble",
          name: "Male",
          legendMarkerType: "circle",
          fillOpacity: .5,
          showInLegend: true,
          toolTipContent: toolTipContent_male,
          dataPoints: dataPoints_male
        },
        {
          type: "bubble",
          legendMarkerType: "circle",
          fillOpacity: .5,
          toolTipContent: toolTipContent_female,
          name: "Female",
          showInLegend: true,
          dataPoints: dataPoints_female
        },
        {
          type: "bubble",
          legendMarkerType: "circle",
          fillOpacity: .0,
          //toolTipContent: "<b>Female</b><br/>Age: {x} yrs<br/> Blood Pressure: {y}<br/> Population: {z}",
          //name: "Female",
          //showInLegend: true,
          dataPoints: [{ x: fake_x, y: fake_y, z: fake_z }]
        }
      ]
    });
    chart.render();
  }

  blood_pressure() {
    this.type = 'blood_pressure';
    let dataPoints_male = [];
    let dataPoints_female = [];
    var count: { [id: string]: {x:number,y:number,z:number,name:string} } = {};
    this.getdataservice.getdata(4).subscribe(
      data => {
        for (let d of data.data) {
          if (count[`${d.age} ${d.value} ${d.sex}`] == undefined) {
            if (d.sex == 0.0) {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'female' };
            }
            else {
              count[`${d.age} ${d.value} ${d.sex}`] = { x: d.age, y: d.value, z: 1, name: 'male' };
            }
          }
          else {
            count[`${d.age} ${d.value} ${d.sex}`].z++;
          }
        }
       
        for (var key in count) {
          if (count[key].name == 'female') {
            dataPoints_female.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
          else {
            dataPoints_male.push({ x: count[key].x, y: count[key].y, z: count[key].z });
          }
        }
        this.continous_bubble_data(dataPoints_male, dataPoints_female, "Blood Pressure vs. Age in Different Sex", "Age", "Blood Pressure",
          "<b>Male</b><br/>Age: {x} yrs<br/> Blood Pressure: {y}<br/> Population: {z}",
          "<b>Female</b><br/>Age: {x} yrs<br/> Blood Pressure: {y}<br/> Population: {z}",
          30,150,60);
      });
  }




  barchat(dataPoints: any, title: string, axisY: string, name: string) {
    console.log(dataPoints);
    let chart = new CanvasJS.Chart(name, {
      animationEnabled: true,
      title: {
        text: title
      },
      axisY: {
        title: axisY
      },
      data: dataPoints
    });
    chart.render();
  }

  blood_sugar_age() {
    this.getdataservice.getdata(6).subscribe(
      data => {
        let max = 0
        for (let d of data.data) {
          if (d.age > max) {
            max = d.age
          }
        }
        let group = Math.ceil(max / 10);
        let dataPoints_false = [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "##0.00\"%\"",
          indexLabel: "{label} {y}",
          dataPoints:[],
        }]

        let dataPoints_true = [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "##0.00\"%\"",
          indexLabel: "{label} {y}",
          dataPoints:[]
        }]
        for (let i = 0; i < group; i++) {
          dataPoints_false[0].dataPoints.push({ y: 0, label: `${i * 10} to ${(i + 1) * 10}` });
          dataPoints_true[0].dataPoints.push({ y: 0, label: `${i * 10} to ${(i + 1) * 10}` })
        }
        let totalmale = 0;
        let totalfemale = 0;
        for (let d of data.data) {
          if (d.value == 1.0) {
            totalmale++;
            dataPoints_true[0].dataPoints[Math.floor(d.age / 10)].y++;
          }
          else {
            totalfemale++;
            dataPoints_false[0].dataPoints[Math.floor(d.age / 10)].y++;
          }
        }
        for (let i = 0; i < group; i++) {
          dataPoints_true[0].dataPoints[i].y = dataPoints_true[0].dataPoints[i].y / totalmale * 100;
          dataPoints_false[0].dataPoints[i].y = dataPoints_true[0].dataPoints[i].y / totalmale * 100;
        }
        console.log(dataPoints_true);
        console.log(dataPoints_false);
        this.pie_chart('chartContainer_pie_true_age', 'Blood Sugar True', dataPoints_true);
        this.pie_chart('chartContainer_pie_false_age', 'Blood Sugar False', dataPoints_false);
      }
    );
  }

  blood_sugar_sex() {
    this.getdataservice.getdata(6).subscribe(
      data => {

        let dataPoints_male = [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "##0.00\"%\"",
          indexLabel: "{label} {y}",
          dataPoints: [],
        }]

        let dataPoints_female = [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "##0.00\"%\"",
          indexLabel: "{label} {y}",
          dataPoints: []
        }]
        dataPoints_male[0].dataPoints.push({ y: 0, label: 'False' });
        dataPoints_male[0].dataPoints.push({ y: 0, label: 'True' });

        dataPoints_female[0].dataPoints.push({ y: 0, label: `False` })
        dataPoints_female[0].dataPoints.push({ y: 0, label: `True` })
        let totalmale = 0;
        let totalfemale = 0;

        for (let d of data.data) {
          if (d.sex == 1.0) {
            totalmale++;
            dataPoints_male[0].dataPoints[Math.floor(d.value)].y++;
          }
          else {
            totalfemale++;
            dataPoints_female[0].dataPoints[Math.floor(d.value)].y++;
          }
        }
        dataPoints_male[0].dataPoints[0].y = dataPoints_male[0].dataPoints[0].y * 100 / totalmale;
        dataPoints_male[0].dataPoints[1].y = dataPoints_male[0].dataPoints[1].y * 100 / totalmale;

        dataPoints_female[0].dataPoints[0].y = dataPoints_female[0].dataPoints[0].y * 100 / totalfemale;
        dataPoints_female[0].dataPoints[1].y = dataPoints_female[0].dataPoints[1].y * 100 / totalfemale;
        console.log(dataPoints_female);
        console.log(dataPoints_male);
        this.pie_chart('chartContainer_pie_male', 'Blood Sugar Male', dataPoints_male);
        this.pie_chart('chartContainer_pie_female', 'Blood Sugar Female', dataPoints_female);
      }
    );
  }

  pie_chart(chart_name: string, title: string, datapoints) {
    var chart = new CanvasJS.Chart(chart_name, {
      animationEnabled: true,
      title: {
        text: title
      },
      data: datapoints
    });
    chart.render();
  }

  electrocardiographic_age() {
    let dataPoints = [];
    this.getdataservice.getdata(7).subscribe(
      data => {
        let max = 0
        for (let d of data.data) {
          if (d.age > max) {
            max = d.age
          }
        }
        let group = Math.ceil(max / 10);
        let group_total = [];
        for (let i = 0; i < group; i++) {
          dataPoints.push({
            type: "bar",
            showInLegend: true,
            name: `${i * 10} to ${(i + 1) * 10} years old`,
            color: this.getRandomColor(i),
            dataPoints: [
              { y: 0, label: "normal" },
              { y: 0, label: "having ST-T wave abnormality" },
              { y: 0, label: "Estes" }]
          });
          group_total.push(0);
        }
        for (let d of data.data) {
          dataPoints[Math.floor(d.age / 10)].dataPoints[(Math.floor(d.value))].y++;
          group_total[Math.floor(d.age / 10)]++;
        }
        for (let i = 0; i < group; i++) {
          for (let d of dataPoints[i].dataPoints) {
            d.y = d.y / group_total[i] * 100;
          }
        }
        this.barchat(dataPoints, 'Electrocardiographic vs. Age', 'Percentage of Population in Each Group', 'chartContainer_age');
      });
  }

  pain_type_age() {
    let dataPoints = [];
    this.getdataservice.getdata(3).subscribe(
      data => {
        let max = 0
        for (let d of data.data) {
          if (d.age > max) {
            max = d.age
          }
        }
        let group = Math.ceil(max / 10);
        let group_total = [];
        for (let i = 0; i < group; i++) {
          dataPoints.push({
            type: "bar",
            showInLegend: true,
            name: `${i * 10} to ${(i + 1) * 10} years old`,
            color: this.getRandomColor(i),
            dataPoints: [
              { y: 0, label: "typical angin" },
              { y: 0, label: "atypical angina" },
              { y: 0, label: "non-anginal pain" },
              { y: 0, label: "asymptomatic" }]
          });
          group_total.push(0);
        }
        for (let d of data.data) {
          dataPoints[Math.floor(d.age / 10)].dataPoints[(Math.floor(d.value - 1))].y++;
          group_total[Math.floor(d.age / 10)]++;
        }
        for (let i = 0; i < group; i++) {
          for (let d of dataPoints[i].dataPoints) {
            d.y = d.y / group_total[i] * 100;
          }
        }
        this.barchat(dataPoints, 'Pain Type vs. Age', 'Percentage of Population in Each Group', 'chartContainer_age');
      });
  }

  electrocardiographic_sex() {
    let dataPoints = [];
    this.getdataservice.getdata(7).subscribe(
      data => {
        dataPoints.push({
          type: "bar",
          showInLegend: true,
          name: 'Female',
          color: '#ff0000',
          dataPoints: [
            { y: 0, label: "normal" },
            { y: 0, label: "having ST-T wave abnormality" },
            { y: 0, label: "Estes" }]
        });
        dataPoints.push({
          type: "bar",
          showInLegend: true,
          name: 'Male',
          color: '#000000',
          dataPoints: [
            { y: 0, label: "normal" },
            { y: 0, label: "having ST-T wave abnormality" },
            { y: 0, label: "Estes" }]
        });

        let male_number = 0
        let female_number = 0
        for (let d of data.data) {
          if (d.sex == 0) {
            female_number++;
          }
          else {
            male_number++;
          }
          dataPoints[Math.floor(d.sex)].dataPoints[(Math.floor(d.value))].y++;
        }
        for (let i = 0; i < 3; i++) {
          dataPoints[0].dataPoints[i].y = dataPoints[0].dataPoints[i].y / female_number * 100
          dataPoints[1].dataPoints[i].y = dataPoints[1].dataPoints[i].y / male_number * 100
        }
        this.barchat(dataPoints, 'Electrocardiographic vs. Sex', 'Percentage of Population in Sex', 'chartContainer_sex');
      });
  }

  pain_type_sex() {
    let dataPoints = [];
    this.getdataservice.getdata(3).subscribe(
      data => {
        dataPoints.push({
            type: "bar",
            showInLegend: true,
            name:'Female',
            color: '#ff0000',
            dataPoints: [
              { y: 0, label: "typical angin" },
              { y: 0, label: "atypical angina" },
              { y: 0, label: "non-anginal pain" },
              { y: 0, label: "asymptomatic" }]
        });
        dataPoints.push({
          type: "bar",
          showInLegend: true,
          name: 'Male',
          color: '#000000',
          dataPoints: [
            { y: 0, label: "typical angin" },
            { y: 0, label: "atypical angina" },
            { y: 0, label: "non-anginal pain" },
            { y: 0, label: "asymptomatic" }]
        });

        let male_number = 0
        let female_number = 0
        for (let d of data.data) {
          if (d.sex == 0) {
            female_number++;
          }
          else {
            male_number++;
          }
          dataPoints[Math.floor(d.sex)].dataPoints[(Math.floor(d.value - 1))].y++;
        }
        for (let i = 0; i < 4; i++) {
          dataPoints[0].dataPoints[i].y = dataPoints[0].dataPoints[i].y / female_number * 100
          dataPoints[1].dataPoints[i].y = dataPoints[1].dataPoints[i].y / male_number * 100
        }
        this.barchat(dataPoints, 'Pain Type vs. Sex', 'Percentage of Population in Sex','chartContainer_sex');
      });
  }
}
