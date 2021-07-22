import { Container, Tab, Tabs } from "@mantine/core";

import { VerilogCodeGenerator } from "./verilog-code-generator";
import { ErrorAnalysis } from "./error-analysis";

export const ToolTabs = () => {
  return (
    <Container style={{ marginTop: 20 }}>
      <Tabs color="dark">
        <Tab label="Verilog Code Generator">
          <VerilogCodeGenerator />
        </Tab>

        <Tab label="Error Analyzer">
          <ErrorAnalysis />
        </Tab>

        <Tab label="Accuracy Analyzer">Accuracy Analyzer</Tab>
      </Tabs>
    </Container>
  );
};
