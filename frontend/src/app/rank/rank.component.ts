import { Component, OnInit } from '@angular/core';
import { GetdataService } from '../getdata.service';
import * as CanvasJS from '../../assets/canvasjs.min';

@Component({
  selector: 'app-rank',
  templateUrl: './rank.component.html',
  styleUrls: ['./rank.component.css']
})
export class RankComponent implements OnInit {

  constructor(private getdataservice: GetdataService,) { }

  ngOnInit() {

  }
  showdata(data,methed) {
    let dataPoints = [];
    for (let key in data) {
      dataPoints.push({ y: data[key], label: key });
    }
    var chart = new CanvasJS.Chart("chartContainer", {
      animationEnabled: true,
      title: {
        text: `Potential Factors Ranking (method ${methed})`
      },
      axisX: {
        interval: 1
      },
      axisY2: {
        interlacedColor: "rgba(1,77,101,.2)",
        gridColor: "rgba(1,77,101,.1)",
        title: "Coefficient"
      },
      data: [{
        type: "bar",
        name: "coefficient",
        axisYType: "secondary",
        //color: "#014D65",
        dataPoints: dataPoints.reverse()
      }]
    });
    chart.render();
  }
  KNN() {
    
    this.getdataservice.getrank("KNN").subscribe(
      data => {
        this.showdata(data,'KNN')
      }
    );
  }

  Drop() {

    this.getdataservice.getrank("Drop").subscribe(
      data => {
        this.showdata(data, 'Drop')
      }
    );
  }
}
