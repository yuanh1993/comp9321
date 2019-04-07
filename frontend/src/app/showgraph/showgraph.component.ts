import { Component, OnInit } from '@angular/core';
import { GetdataService } from '../getdata.service';
import * as CanvasJS from '../../assets/canvasjs.min';
import { all } from 'q';
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
        }
        for (let d of data.data) {
          dataPoints[Math.floor(d.age / 10)].dataPoints[(Math.floor(d.value - 1))].y++;
        }
        this.barchat(dataPoints, 'Pain Type vs. Age', 'Population', 'chartContainer_age');
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


        for (let d of data.data) {
          dataPoints[Math.floor(d.sex)].dataPoints[(Math.floor(d.value - 1))].y++;
        }
        this.barchat(dataPoints, 'Pain Type vs. Sex', 'Population','chartContainer_sex');
      });
  }

}
