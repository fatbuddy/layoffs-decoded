import { Card, Grid, BadgeDelta, Flex,
    Metric,
    ProgressBar,
    Text} from "@tremor/react";

export default function Question2() {
  return (
    <>
        <Grid
        numColsLg={2}
        numColsLg={3}
        className="mt-6 gap-6"
        >
        <Card>
            <Flex alignItems="start">
                <div>
                <Text>Sales</Text>
                <Metric>$ 12,699</Metric>
                </div>
                <BadgeDelta deltaType="moderateIncrease">13.2%</BadgeDelta>
            </Flex>
            <Flex className="mt-4">
                <Text className="truncate">68% ($ 149,940)</Text>
                <Text> $ 220,500 </Text>
            </Flex>
            <ProgressBar percentageValue={15.9} className="mt-2" />
        </Card>
        <Card>
            <Flex alignItems="start">
                <div>
                <Text>Sales</Text>
                <Metric>$ 12,699</Metric>
                </div>
                <BadgeDelta deltaType="moderateIncrease">13.2%</BadgeDelta>
            </Flex>
            <Flex className="mt-4">
                <Text className="truncate">68% ($ 149,940)</Text>
                <Text> $ 220,500 </Text>
            </Flex>
            <ProgressBar percentageValue={15.9} className="mt-2" />
        </Card>
        <Card>
            <Flex alignItems="start">
                <div>
                <Text>Sales</Text>
                <Metric>$ 12,699</Metric>
                </div>
                <BadgeDelta deltaType="moderateIncrease">13.2%</BadgeDelta>
            </Flex>
            <Flex className="mt-4">
                <Text className="truncate">68% ($ 149,940)</Text>
                <Text> $ 220,500 </Text>
            </Flex>
            <ProgressBar percentageValue={15.9} className="mt-2" />
        </Card>
        </Grid>
    </>
  );
}