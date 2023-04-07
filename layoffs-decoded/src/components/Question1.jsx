import { Toggle, ToggleItem, Card, Grid, Title, DonutChart, List, ListItem, Subtitle  } from "@tremor/react";
import {ChartPieIcon, ChartBarIcon, ChartSquareBarIcon, PresentationChartBarIcon, PresentationChartLineIcon} from "@heroicons/react/outline";
import ChartView from "./ChartView";
import React, { useEffect, useState } from "react"

const valueFormatter = (number) =>
`${Intl.NumberFormat("us").format(number).toString()}`;


export default function Question1() {
  const [precovidStatus, setPrecovidStatus] = useState('');
  const [precovid, setPrecovid] = useState([]);
  const [covidStatus, setCovidStatus] = useState('');
  const [covid, setCovid] = useState([]);
  const [postcovidStatus, setPostcovidStatus] = useState('');
  const [postcovid, setPostcovid] = useState([]);

  function callApis(technique) {
    setPrecovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_precovid_'+ technique + '?limit=10')
    .then(result => result.json())
    .then(data => setPrecovid(data.payload))
    .then(()=>setPrecovidStatus('Success'))
    .catch(()=>setPrecovidStatus('Error'));

    setCovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_covid_'+ technique + '?limit=10')
    .then(result => result.json())
    .then(data => setCovid(data.payload))
    .then(()=>setCovidStatus('Success'))
    .catch(()=>setCovidStatus('Error'));

    setPostcovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_postcovid_'+ technique + '?limit=10')
    .then(result => result.json())
    .then(data => setPostcovid(data.payload))
    .then(()=>setPostcovidStatus('Success'))
    .catch(()=>setPostcovidStatus('Error'));
  }

  useEffect(()=>{
    setPrecovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_precovid_pearson?limit=10')
    .then(result => result.json())
    .then(data => setPrecovid(data.payload))
    .then(()=>setPrecovidStatus('Success'))
    .catch(()=>setPrecovidStatus('Error'));

    setCovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_covid_pearson?limit=10')
    .then(result => result.json())
    .then(data => setCovid(data.payload))
    .then(()=>setCovidStatus('Success'))
    .catch(()=>setCovidStatus('Error'));

    setPostcovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_postcovid_pearson?limit=10')
    .then(result => result.json())
    .then(data => setPostcovid(data.payload))
    .then(()=>setPostcovidStatus('Success'))
    .catch(()=>setPostcovidStatus('Error'));
    }, []);

  return (
    <>
        <Toggle defaultValue="pearson" onValueChange={(value) => callApis(value)}>
          <ToggleItem value="pearson" text="Pearson" icon={ChartPieIcon} />
          <ToggleItem value="spearman" text="Spearman" icon={ChartBarIcon} />
          <ToggleItem value="lasso" text="Lasso" icon={ChartSquareBarIcon} />
          <ToggleItem value="ridge" text="Ridge" icon={PresentationChartBarIcon} />
          <ToggleItem value="decisiontree" text="Decision Tree" icon={PresentationChartLineIcon} />
          <ToggleItem value="elasticnet" text="Elastic Net" icon={ChartPieIcon} />
          <ToggleItem value="randomforest" text="Random Forest" icon={ChartBarIcon} />
        </Toggle>
        <Grid
        numColsLg={3}
        className="mt-6 gap-6"
        >
        <Card>
            <Title>Precovid</Title>
            {precovidStatus === 'Loading' && <DonutChart
            className="mt-6"
            showLabel={true}
            label="Loading..."
            />}
            {precovidStatus === 'Success' && 
            <DonutChart
            className="mt-6"
            variant="pie"
            data={precovid}
            category="value"
            index="name"
            valueFormatter={valueFormatter}
            colors={["slate", "violet", "indigo", "rose", "cyan", "amber", "teal", "orange", "fuchsia", "pink"]}
            />}
        </Card>
        <Card>
            <Title>Covid</Title>
            {covidStatus === 'Loading' && <DonutChart
            className="mt-6"
            showLabel={true}
            label="Loading..."
            />}
            {covidStatus === 'Success' &&
            <DonutChart
            className="mt-6"
            data={covid}
            category="value"
            index="name"
            valueFormatter={valueFormatter}
            colors={["slate", "violet", "indigo", "rose", "cyan", "amber", "teal", "orange", "fuchsia", "pink"]}
            />}
        </Card>
        <Card>
            <Title>Postcovid</Title>
            {postcovidStatus === 'Loading' && <DonutChart
            className="mt-6"
            showLabel={true}
            label="Loading..."
            />}
            {postcovidStatus === 'Success' &&
            <DonutChart
            className="mt-6"
            variant="pie"
            data={postcovid}
            category="value"
            index="name"
            valueFormatter={valueFormatter}
            colors={["slate", "violet", "indigo", "rose", "cyan", "amber", "teal", "orange", "fuchsia", "pink"]}
            />}
        </Card>
        </Grid>
        <Grid
        numColsLg={3}
        className="mt-6 gap-6"
        >
        <Card>
            <Title>Precovid</Title>
            <List>
            {precovid.map((item) => (
                <ListItem key={item.name}>
                <span>{item.name}</span>
                <span>{item.value}</span>
                </ListItem>
            ))}
            </List>
        </Card>
        <Card>
            <Title>Covid</Title>
            <List>
            {covid.map((item) => (
                <ListItem key={item.name}>
                <span>{item.name}</span>
                <span>{item.value}</span>
                </ListItem>
            ))}
            </List>
        </Card>
        <Card>
            <Title>Postcovid</Title>
            <List>
            {postcovid.map((item) => (
                <ListItem key={item.name}>
                <span>{item.name}</span>
                <span>{item.value}</span>
                </ListItem>
            ))}
            </List>
        </Card>
        </Grid>

        <div className="mt-6">
        <ChartView/>
        </div>
    </>
  );
}