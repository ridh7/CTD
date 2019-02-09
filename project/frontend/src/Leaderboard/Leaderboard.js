import React from 'react'
import styled from 'styled-components'
import { css } from '@emotion/core';
import { ClipLoader } from 'react-spinners';


const AppWrapper = styled.div`
         border: 2px solid green;
         width:10vw;
         height:10vh;
         display:flex;
    `;
const override = css`
    display: block;
    margin: 0 auto;
    border-color: red;
`;
const Test= styled.p`
    width:20vw;
`;
class Leaderboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true
        }
    }
    render() {
        return (

            <section className="container-fluid bigbody">
                <AppWrapper>
                  <Test> TEST CASE 1:</Test>
                  <Test>
                  <ClipLoader
                        css={override}
                        sizeUnit={"vh"}
                        size={5}
                        color={'#123abc'}
                        loading={this.state.loading}
                    />
                  </Test>
                
                </AppWrapper>
            </section>
        )
    }




}

export default Leaderboard

