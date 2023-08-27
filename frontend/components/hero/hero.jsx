import React from 'react';
import { Search } from '../search/search';
import styles from './hero.module.css';

export class Hero extends React.Component {

    constructor(props) {
        super(props);
        this.state = { query: "" };
    }

    render() {
        return (
            <div className={styles.hero}>
                <div className={styles.mainTitle}>
                    <h2>Preguntale al candidato</h2>
                    <h4>Presidenciales 2023</h4>
                    <div className={styles.subTitle}>
                        <p>Usá inteligencia artificial para hacerle preguntas a los candidatos presidenciales</p>
                    </div>
                </div>
                <div className={styles.search}>
                    <Search />
                </div>
            </div >
        );
    }
}

