import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof OriginalLayout>;

export default function LayoutWrapper(props: Props): JSX.Element {
  return (
    <>
   
      <OriginalLayout {...props} />
      
    </>
  );
}