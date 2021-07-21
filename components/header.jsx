import { Group, Col, Button, Container, Text, Title } from "@mantine/core";
import { RiBookReadLine } from "react-icons/ri";

export const Header = () => {
  return (
    <Container style={{ marginTop: 20 }}>
      <Group position="apart">
        <Col span={8}>
          <Title order={1}>Approximate Computing Tool</Title>
          <Text>Web-application version of Approximate Computing Tool</Text>
        </Col>
        <Col span={4}>
          <Button
            component="a"
            leftIcon={<RiBookReadLine />}
            variant="outline"
            color="dark"
            target="_blank"
            href="https://tool-documentation.vercel.app"
          >
            Documentation
          </Button>
        </Col>
      </Group>
    </Container>
  );
};
