import { Card, Grid,
    Text,
    Title,
    Table,
    TableHead,
    TableRow,
    TableHeaderCell,
    TableBody,
    TableCell} from "@tremor/react";
import shapGBT from '../public/SHAP-summary-GBT.png';
import shapRF from '../public/SHAP-summary-RF.png';
import React, { useEffect, useState } from "react";

export default function Question2() {

  const [modelMetrics, setModelMetrics] = useState([]);

  useEffect(()=>{
    fetch(process.env.REACT_APP_API_PROXY + '/q2_model_metrics?limit=10')
    .then(result => result.json())
    .then(data => setModelMetrics(data.payload));
  }, []);

  return (
    <>
        <Grid
        numColsLg={2}
        className="mt-6 gap-6"
        >
            <Card>
                <Title>Gradient Boost SHAP</Title>
                <img src={shapGBT} alt="shap gbt" />
            </Card>
            <Card>
                <Title>Random Forest SHAP</Title>
                <img src={shapRF} alt="shap rf" />
            </Card>
            </Grid>
        <Grid
        className="mt-6 gap-6"
        >
            <Card>
                <Title>Regression Model Metrics</Title>
                <Table className="mt-5">
                <TableHead>
                    <TableRow>
                        <TableHeaderCell>Metric</TableHeaderCell>
                        <TableHeaderCell>Decision Tree</TableHeaderCell>
                        <TableHeaderCell>Random Forest</TableHeaderCell>
                        <TableHeaderCell>Gradient Boosting Reg</TableHeaderCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {modelMetrics.map((item) => (
                    <TableRow key={item.metric}>
                        <TableCell>{item.metric}</TableCell>
                        <TableCell><Text>{item['decision tree']}</Text></TableCell>
                        <TableCell><Text>{item['random forest']}</Text></TableCell>
                        <TableCell><Text>{item['gradient boosting reg']}</Text></TableCell>
                    </TableRow>
                    ))}
                </TableBody>
                </Table>
            </Card>
        </Grid>
    </>
  );
}