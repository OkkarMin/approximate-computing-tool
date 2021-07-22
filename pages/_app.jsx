import { useEffect } from "react";
import Head from "next/head";
import { JssProvider, createGenerateId } from "react-jss";
import { MantineProvider, NormalizeCSS, GlobalStyles } from "@mantine/core";

export default function App(props) {
  const { Component, pageProps } = props;

  useEffect(() => {
    const jssStyles = document.getElementById("mantine-ssr-styles");
    if (jssStyles) {
      jssStyles?.parentElement?.removeChild(jssStyles);
    }
  }, []);

  return (
    <>
      <JssProvider generateId={createGenerateId({ minify: true })}>
        <Head>
          <title>Approximate Computing Tool</title>
          <meta
            name="viewport"
            content="minimum-scale=1, initial-scale=1, width=device-width"
          />
        </Head>

        <MantineProvider
          theme={{
            /** Put your mantine theme override here */
            colorScheme: "light",
          }}
        >
          <NormalizeCSS />
          <GlobalStyles />
          <Component {...pageProps} />
        </MantineProvider>
      </JssProvider>
    </>
  );
}
