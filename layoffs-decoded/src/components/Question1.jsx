import { Card, Grid, LineChart, Title, DonutChart, List, ListItem } from "@tremor/react";
import ChartView from "./ChartView";

const chartdata = [
    {
      year: 1951,
      "Population growth rate": 1.74,
    },
    {
      year: 1952,
      "Population growth rate": 1.93,
    },
    {
      year: 1953,
      "Population growth rate": 1.9,
    },
    {
      year: 1954,
      "Population growth rate": 1.98,
    },
    {
      year: 1955,
      "Population growth rate": 2,
    },
];

const cities = [
    {
      name: "New York",
      sales: 9800,
    },
    {
      name: "London",
      sales: 4567,
    },
    {
      name: "Hong Kong",
      sales: 3908,
    },
    {
      name: "San Francisco",
      sales: 2400,
    },
    {
      name: "Singapore",
      sales: 1908,
    },
    {
      name: "Zurich",
      sales: 1398,
    },
  ];

  export const performance = [
    {
      date: "2021-01-01",
      Sales: 900.73,
      Profit: 173,
      Customers: 73,
    },
    {
      date: "2021-01-02",
      Sales: 1000.74,
      Profit: 174.6,
      Customers: 74,
    },
    // ...
    {
      date: "2021-03-13",
      Sales: 882,
      Profit: 682,
      Customers: 682,
    },
  ];
  
const valueFormatter = (number) =>
`$ ${Intl.NumberFormat("us").format(number).toString()}`;


const dataFormatter = (number) =>
`${Intl.NumberFormat("us").format(number).toString()}%`;


export default function Question1() {
  return (
    <>
        <Grid
        numColsLg={3}
        className="mt-6 gap-6"
        >
        <Card>
            <Title>Population growth rate (1951 to 2021)</Title>
            <LineChart
            className="mt-6"
            data={chartdata}
            index="year"
            categories={["Population growth rate"]}
            colors={["blue"]}
            valueFormatter={dataFormatter}
            yAxisWidth={40}
            />
        </Card>
        <Card>
            <Title>Sales</Title>
            <DonutChart
            className="mt-6"
            data={cities}
            category="sales"
            index="name"
            valueFormatter={valueFormatter}
            colors={["slate", "violet", "indigo", "rose", "cyan", "amber"]}
            />
        </Card>
        <Card>
            <Title>Tremor's Hometowns</Title>
            <List>
            {cities.map((item) => (
                <ListItem key={item.name}>
                <span>{item.name}</span>
                <span>{item.sales}</span>
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