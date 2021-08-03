import { Container, Tab, Tabs } from "@mantine/core";

import { VerilogCodeGenerator } from "./verilog-code-generator";
import { ErrorAnalyzer } from "./error-analyzer";

export const ToolTabs = () => {
  return (
    <Container style={{ marginTop: 20 }}>
      <Tabs color="dark">
        <Tab label="Verilog Code Generator">
          <VerilogCodeGenerator />
        </Tab>

        <Tab label="Error Analyzer">
          <ErrorAnalyzer />
        </Tab>

        <Tab label="Accuracy Analyzer">Accuracy Analyzer</Tab>
      </Tabs>
    </Container>
  );
};
