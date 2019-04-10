import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({
    'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
    'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    'Access-Control-Allow-Headers': 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token',
  }),
  withCredentials: true,
  //observe: 'response',
}

@Injectable({
  providedIn: 'root'

})
export class GetdataService {
  baseurl="http://127.0.0.1:5000/api"
  constructor(
  private http: HttpClient,
  ) {}
  getdata(id:number){
    return this.http.get<any>(`${this.baseurl}/getData/${id}`);
  }
  getrank(method: string) {
    return this.http.get<any>(`${this.baseurl}/rankFeature?method=${method}`);
  }
  getcurve(model_type: string) {
    return this.http.get<any>(`${this.baseurl}/getCurve?model_type=${model_type}`);
  }
  predict(model_type: string,
                age: string,
                sex: string,
                pain_type: string,
                blood_pressure: string,
                cholestoral: string,
                blood_sugar: string,
                electrocardiographic: string,
                heart_rate: string,
                angina: string,
                oldpeak: string,
                ST_segment: string,
                vessels: string,
                thal: string) {
    return this.http.get<any>(`${this.baseurl}/DataPredict?model_type=${model_type}&age=${age}&sex=${sex}&pain_type=${pain_type}&blood_pressure=${blood_pressure}&cholestoral=${cholestoral}&blood_sugar=${blood_sugar}&electrocardiographic=${electrocardiographic}&heart_rate=${heart_rate}&angina=${angina}&oldpeak=${oldpeak}&ST_segment=${ST_segment}&vessels=${vessels}&thal=${thal}`);
  }
  getcluster(cluster_method: string) {
    return this.http.get<any>(`${this.baseurl}/get_clustering?cluster_method=${cluster_method}`);
  }
}
