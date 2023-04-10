import { Toggle, ToggleItem, Card, Grid, Title, DonutChart, BarChart, List, ListItem, Subtitle } from "@tremor/react";
import { ChartPieIcon, ChartBarIcon, ChartSquareBarIcon, PresentationChartBarIcon, PresentationChartLineIcon } from "@heroicons/react/outline";
import ChartView from "./ChartView";
import React, { useEffect, useState } from "react"
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


export default function Question1Wrapper({ val, precovid, covid, postcovid, precovidStatus, covidStatus, postcovidStatus }) {

    return (
        <>
            {val == "backward_elimination" &&
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
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {precovid.map((item) => (
                                    <TableRow key={item.feature_name}>
                                        <TableCell>
                                            <Text>{item.feature_name}</Text>
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
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {covid.map((item) => (
                                    <TableRow key={item.feature_name}>
                                        <TableCell>
                                            <Text>{item.feature_name}</Text>
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
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {postcovid.map((item) => (
                                    <TableRow key={item.feature_name}>
                                        <TableCell>
                                            <Text>{item.feature_name}</Text>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Card>
                </Grid>
            }
            {val != "backward_elimination" &&
                <Grid
                    numColsLg={2}
                    className="mt-6 gap-6"
                >
                    <Card>
                        <Title>Precovid</Title>
                        {precovidStatus === 'Loading' && <BarChart
                            className="mt-6"
                            showlabel="true"
                            label="Loading..." />}
                        {precovidStatus === 'Success' &&
                            <BarChart
                                className="mt-6"
                                data={precovid}
                                index="label"
                                categories={["average_score"]}
                                colors={["teal"]}
                                valueFormatter={valueFormatter}
                                yAxisWidth={40} />}
                    </Card>
                    <Card>
                        <Title>Precovid</Title>
                        <Table className="mt-5">
                            <TableHead>
                                <TableRow>
                                    <TableHeaderCell>Label</TableHeaderCell>
                                    <TableHeaderCell>Feature Name</TableHeaderCell>
                                    <TableHeaderCell>Average Score</TableHeaderCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {precovid.map((item) => (
                                    <TableRow key={item.label}>
                                        <TableCell>{item.label}</TableCell>
                                        <TableCell>
                                            <Text>{item.feature_name}</Text>
                                        </TableCell>
                                        <TableCell>
                                            <Text>{item.average_score}</Text>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Card>
                </Grid>
            }
            {val != "backward_elimination" &&
                <Grid
                    numColsLg={2}
                    className="mt-6 gap-6"
                >
                    <Card>
                        <Title>Covid</Title>
                        {covidStatus === 'Loading' && <BarChart
                            className="mt-6"
                            showlabel="true"
                            label="Loading..." />}
                        {covidStatus === 'Success' &&
                            <BarChart
                                className="mt-6"
                                data={covid}
                                index="label"
                                categories={["average_score"]}
                                colors={["teal"]}
                                valueFormatter={valueFormatter}
                                yAxisWidth={40} />}
                    </Card>
                    <Card>
                        <Title>Covid</Title>
                        <Table className="mt-5">
                            <TableHead>
                                <TableRow>
                                    <TableHeaderCell>Label</TableHeaderCell>
                                    <TableHeaderCell>Feature Name</TableHeaderCell>
                                    <TableHeaderCell>Average Score</TableHeaderCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {covid.map((item) => (
                                    <TableRow key={item.label}>
                                        <TableCell>{item.label}</TableCell>
                                        <TableCell>
                                            <Text>{item.feature_name}</Text>
                                        </TableCell>
                                        <TableCell>
                                            <Text>{item.average_score}</Text>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Card>
                </Grid>
            }
            {val != "backward_elimination" &&
                <Grid
                    numColsLg={2}
                    className="mt-6 gap-6"
                >
                    <Card>
                        <Title>Postcovid</Title>
                        {postcovidStatus === 'Loading' && <BarChart
                            className="mt-6"
                            showlabel="true"
                            label="Loading..." />}
                        {postcovidStatus === 'Success' &&
                            <BarChart
                                className="mt-6"
                                data={postcovid}
                                index="label"
                                categories={["average_score"]}
                                colors={["teal"]}
                                valueFormatter={valueFormatter}
                                yAxisWidth={40} />}
                    </Card>
                    <Card>
                        <Title>Postcovid</Title>
                        <Table className="mt-5">
                            <TableHead>
                                <TableRow>
                                    <TableHeaderCell>Label</TableHeaderCell>
                                    <TableHeaderCell>Feature Name</TableHeaderCell>
                                    <TableHeaderCell>Average Score</TableHeaderCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {postcovid.map((item) => (
                                    <TableRow key={item.label}>
                                        <TableCell>{item.label}</TableCell>
                                        <TableCell>
                                            <Text>{item.feature_name}</Text>
                                        </TableCell>
                                        <TableCell>
                                            <Text>{item.average_score}</Text>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Card>
                </Grid>
            }</>
    );

}