import { Toggle, ToggleItem, Card, Grid, Title, DonutChart, BarChart, List, ListItem, Subtitle } from "@tremor/react";
import { ChartPieIcon, ChartBarIcon, ChartSquareBarIcon, PresentationChartBarIcon, PresentationChartLineIcon } from "@heroicons/react/outline";
import ChartView from "./ChartView";
import React, { useEffect, useState } from "react"
import Question1Wrapper from './Question1Wrapper';
import {
  Text,
  Table,
  TableHead,
  TableHeaderCell,
  TableBody,
  TableRow,
  TableCell,
} from "@tremor/react";

const valueFormatter = (number) =>
  `${Intl.NumberFormat("us").format(number).toString()}`;


export default function Question1() {
  const [binLayoffs, setBinLayoffs] = useState([]);
  const [precovidStatus, setPrecovidStatus] = useState('');
  const [precovid, setPrecovid] = useState([]);
  const [covidStatus, setCovidStatus] = useState('');
  const [covid, setCovid] = useState([]);
  const [postcovidStatus, setPostcovidStatus] = useState('');
  const [postcovid, setPostcovid] = useState([]);
  const [val, setVal] = useState([]);

  function callApis(technique) {
    setPrecovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_precovid_' + technique + '?limit=10')
      .then(result => result.json())
      .then(data => setPrecovid(data.payload))
      .then(() => setVal(technique))
      .then(() => setPrecovidStatus('Success'))
      .catch(() => setPrecovidStatus('Error'));

    setCovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_covid_' + technique + '?limit=10')
      .then(result => result.json())
      .then(data => setCovid(data.payload))
      .then(() => setVal(technique))
      .then(() => setCovidStatus('Success'))
      .catch(() => setCovidStatus('Error'));

    setPostcovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_postcovid_' + technique + '?limit=10')
      .then(result => result.json())
      .then(data => setPostcovid(data.payload))
      .then(() => setVal(technique))
      .then(() => setPostcovidStatus('Success'))
      .catch(() => setPostcovidStatus('Error'));
  }

  useEffect(() => {
    fetch(process.env.REACT_APP_API_PROXY + '/q1_bin_layoffs?limit=10')
      .then(result => result.json())
      .then(data => setBinLayoffs(data.payload));

    setPrecovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_precovid_pearson?limit=10')
      .then(result => result.json())
      .then(data => setPrecovid(data.payload))
      .then(() => setPrecovidStatus('Success'))
      .catch(() => setPrecovidStatus('Error'));

    setCovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_covid_pearson?limit=10')
      .then(result => result.json())
      .then(data => setCovid(data.payload))
      .then(() => setCovidStatus('Success'))
      .catch(() => setCovidStatus('Error'));

    setPostcovidStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q1_postcovid_pearson?limit=10')
      .then(result => result.json())
      .then(data => setPostcovid(data.payload))
      .then(() => setPostcovidStatus('Success'))
      .catch(() => setPostcovidStatus('Error'));
  }, []);

  return (
    <>
      <Toggle defaultValue="pearson" style={{ "flexWrap": "wrap" }} onValueChange={(value) => callApis(value)}>
        <ToggleItem value="pearson" text="Pearson" icon={ChartPieIcon} />
        <ToggleItem value="spearman" text="Spearman" icon={ChartBarIcon} />
        <ToggleItem value="lasso" text="Lasso" icon={ChartSquareBarIcon} />
        <ToggleItem value="ridge" text="Ridge" icon={PresentationChartBarIcon} />
        <ToggleItem value="decisiontree" text="Decision Tree" icon={PresentationChartLineIcon} />
        <ToggleItem value="elasticnet" text="Elastic Net" icon={ChartPieIcon} />
        <ToggleItem value="randomforest" text="Random Forest" icon={ChartBarIcon} />
        <ToggleItem value="forward_elimination" text="Forward Elimination" icon={ChartSquareBarIcon} />
        <ToggleItem value="backward_elimination" text="Backward Elimination" icon={PresentationChartBarIcon} />
        <ToggleItem value="stepwise_elimination" text="Stepwise Elimination" icon={PresentationChartLineIcon} />
      </Toggle>
      {val != "forward_elimination" && val != "stepwise_elimination" && val != "backward_elimination" &&
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
      }
      {val != "forward_elimination" && val != "stepwise_elimination" && val != "backward_elimination" &&
        <Grid
          numColsLg={3}
          className="mt-6 gap-6"
        >
          <Card>
            <Title>Precovid</Title>
            <Table className="mt-5">
              <TableHead>
                <TableRow>
                  <TableHeaderCell>Feature Name</TableHeaderCell>
                  <TableHeaderCell>Average Score</TableHeaderCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {precovid.map((item) => (
                  <TableRow key={item.name}>
                    <TableCell>{item.name}</TableCell>
                    <TableCell>
                      <Text>{item.value}</Text>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
          <Card>
            <Title>Covid</Title>
            <Table className="mt-5">
              <TableHead>
                <TableRow>
                  <TableHeaderCell>Feature Name</TableHeaderCell>
                  <TableHeaderCell>Average Score</TableHeaderCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {covid.map((item) => (
                  <TableRow key={item.name}>
                    <TableCell>{item.name}</TableCell>
                    <TableCell>
                      <Text>{item.value}</Text>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
          <Card>
            <Title>Postcovid</Title>
            <Table className="mt-5">
              <TableHead>
                <TableRow>
                  <TableHeaderCell>Feature Name</TableHeaderCell>
                  <TableHeaderCell>Average Score</TableHeaderCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {postcovid.map((item) => (
                  <TableRow key={item.name}>
                    <TableCell>{item.name}</TableCell>
                    <TableCell>
                      <Text>{item.value}</Text>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        </Grid>
      }
      {(val == "forward_elimination" || val == "stepwise_elimination" || val == "backward_elimination") &&
        <Question1Wrapper val={val} precovid={precovid} covid={covid} postcovid={postcovid} precovidStatus={precovidStatus} covidStatus={covidStatus} postcovidStatus={postcovidStatus}></Question1Wrapper>
      }

      <Grid
          className="mt-6 gap-6"
        >
          <Card>
            <Title>Number of Layoffs during each Time Period</Title>
            <BarChart
              className="mt-6"
              data={binLayoffs}
              index="time_period"
              categories={["employees_laidoff"]}
              colors={["amber"]}
              valueFormatter={valueFormatter}
              yAxisWidth={48}
            />
          </Card>
      </Grid>
    </>
  );
}