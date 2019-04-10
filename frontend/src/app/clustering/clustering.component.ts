import { Component, OnInit } from '@angular/core';
import { GetdataService } from '../getdata.service';
import * as CanvasJS from '../../assets/canvasjs.min';

@Component({
  selector: 'app-clustering',
  templateUrl: './clustering.component.html',
  styleUrls: ['./clustering.component.css']
})
export class ClusteringComponent implements OnInit {

  constructor(private getdataservice: GetdataService, ) { }

  ngOnInit() {
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
    let dataPoints01 = [];
    let dataPoints00 = [];
    let dataPoints10 = [];
    let dataPoints11 = [];
    for (let line in data["data"]) {
      
      if (data["data"][line]["cluster"] == 0) {
        if (data["data"][line]["target"] == 0) {
          dataPoints00.push({ x: data["data"][line]["label_1"], y: data["data"][line]["label_2"] });
        } else {
          dataPoints01.push({ x: data["data"][line]["label_1"], y: data["data"][line]["label_2"] });
        }
      } else {
        if (data["data"][line]["target"] == 0) {
          dataPoints10.push({ x: data["data"][line]["label_1"], y: data["data"][line]["label_2"] });
        } else {
          dataPoints11.push({ x: data["data"][line]["label_1"], y: data["data"][line]["label_2"] });
        }
      }
    }
    var chart = new CanvasJS.Chart("chartContainer", {
      animationEnabled: true,
      title: {
        text: `Clustering with ${methed}`
      },
      axisX: {
        title: "Component 1"
      },
      axisY: {
        title: "Component 2"
      },
      legend: {
        cursor: "pointer",
        itemclick: this.toggleDataSeries
      },
      data: [{
        type: "scatter",
        name: "Cluster 1: has disease",
        markerColor: "red",
        showInLegend: true,
        toolTipContent: "<span style=\"color:#4F81BC \">{name}</span><br>Component 1: {x}<br>Component 2: {y}",
        dataPoints: dataPoints01
      },
      {
        type: "scatter",
        name: "Cluster 1: no disease",
        markerColor: "red",
        showInLegend: true,
        markerType: "triangle",
        toolTipContent: "<span style=\"color:#C0504E \">{name}</span><br>Component 1: {x}<br>Component 2: {y}",
        dataPoints: dataPoints00
      },
      {
        type: "scatter",
        name: "Cluster 2: has disease",
        markerColor: "blue",
        showInLegend: true,
        toolTipContent: "<span style=\"color:#4F81BC \">{name}</span><br>Component 1: {x}<br>Component 2: {y}",
        dataPoints: dataPoints11
      },
      {
        type: "scatter",
        name: "Cluster 2: no disease",
        markerColor: "blue",
        showInLegend: true,
        markerType: "triangle",
        toolTipContent: "<span style=\"color:#4F81BC \">{name}</span><br>Component 1: {x}<br>Component 2: {y}",
        dataPoints: dataPoints10
      },
      ]
    });
    chart.render();
  }

  kmeans() {
    this.getdataservice.getcluster("kmeans").subscribe(
      data => {
        this.showdata(data, 'kmeans')
      }
    );
  }

  spectral() {
    this.getdataservice.getcluster("spectral").subscribe(
      data => {
        this.showdata(data, 'spectral')
      }
    );
  }

}
