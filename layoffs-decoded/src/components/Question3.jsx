import { Card, 
    Grid, 
    Text,
    Title,
    BarList, 
    Bold, 
    Flex,
    DonutChart,
    BarChart} from "@tremor/react";
import React, { useEffect, useState } from "react";

const valueFormatter = (number) =>
`${Intl.NumberFormat("us").format(number).toString()}`;

export default function Question3() {
  const [titlesStatus, setTitlesStatus] = useState('');
  const [titles, setTitles] = useState([]);
  const [departmentStatus, setDepartmentStatus] = useState('');
  const [department, setDepartments] = useState([]);
  const [locationStatus, setLocationStatus] = useState('');
  const [location, setLocations] = useState([]);

  useEffect(()=>{
    setTitlesStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q3_titles?limit=10')
    .then(result => result.json())
    .then(data => setTitles(data.payload))
    .then(()=>setTitlesStatus('Success'))
    .catch(()=>setTitlesStatus('Error'));

    setDepartmentStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q3_departments?limit=10')
    .then(result => result.json())
    .then(data => setDepartments(data.payload))
    .then(()=>setDepartmentStatus('Success'))
    .catch(()=>setDepartmentStatus('Error'));

    setLocationStatus('Loading');
    fetch(process.env.REACT_APP_API_PROXY + '/q3_locations?limit=10')
    .then(result => result.json())
    .then(data => setLocations(data.payload))
    .then(()=>setLocationStatus('Success'))
    .catch(()=>setLocationStatus('Error'));
    }, []);
    
  return (
    <>
        <Grid
        numColsLg={2}
        className="mt-6 gap-6"
        >
        <Card>
            <Title>Top Titles Which Laid Off</Title>
            {titlesStatus === 'Loading' && <DonutChart
            className="mt-6"
            showLabel={true}
            label="Loading..."
            />}
            {titlesStatus === 'Success' &&
            <Flex className="mt-4">
            <Text>
                <Bold>Title</Bold>
            </Text>
            <Text>
                <Bold>Number of Layoffs</Bold>
            </Text>
            </Flex>}
            {titlesStatus === 'Success' &&
            <BarList data={titles} className="mt-2" />}
        </Card>
        <Card>
            <Title>Top Departments Which Laid Off</Title>
            {departmentStatus === 'Loading' && <DonutChart
            className="mt-6"
            showLabel={true}
            label="Loading..."
            />}
            {departmentStatus === 'Success' &&
            <Flex className="mt-4">
            <Text>
                <Bold>Title</Bold>
            </Text>
            <Text>
                <Bold>Number of Layoffs</Bold>
            </Text>
            </Flex>}
            {departmentStatus === 'Success' &&
            <BarList data={department} className="mt-2" />}
        </Card>
        </Grid>

        <div className="mt-6">
        <Card>
            <Title>Top Countries Which Laid Off</Title>
            {locationStatus === 'Loading' && <DonutChart
            className="mt-6"
            showLabel={true}
            label="Loading..."
            />}
            {locationStatus === 'Success' &&
            <Flex className="mt-4">
            <Text>
                <Bold>Country</Bold>
            </Text>
            <Text>
                <Bold>Number of Layoffs</Bold>
            </Text>
            </Flex>}
            {locationStatus === 'Success' &&
            <BarList data={location} className="mt-2" />}
        </Card>
        </div>
    </>
  );
}