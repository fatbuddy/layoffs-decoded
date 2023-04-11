import { useState } from "react";
import { Metric, Tab, TabList, Text, Title } from "@tremor/react";
import Question1 from './Question1';
import Question2 from './Question2';
import Question3 from './Question3';


export default function Dashboard() {

  const [selectedView, setSelectedView] = useState("1");
  return (
    <main className="bg-slate-50 p-6 sm:p-10">
      <Metric>Layoffs Decoded</Metric>
  
      <TabList
        defaultValue="1"
        onValueChange={(value) => setSelectedView(value)}
        margintop="mt-6"
      >
        <Tab value="1" text="COVID Metrics" />
        <Tab value="2" text="Predictive Company Metrics" />
        <Tab value="3" text="Employee Profile Metrics" />
      </TabList>

      {(function() {
        switch(selectedView) {
          case "1":
            return (
              <Question1/>
            );
          case "2":
            return (
              <Question2/>
            );
          case "3":
            return (
              <Question3/>
            ); 
          default:
            return (
              <Question1/>
            );
         }
        }
      )()}
    </main>
  );
}