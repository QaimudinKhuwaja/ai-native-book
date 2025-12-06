import React from 'react';

function HomeHero() {
  return (
    <div className="hero hero--primary hero--showcase">
      <div className="container text--center">
        <h1 className="hero__title">Welcome to the AI-Native Book!</h1>
        <p className="hero__subtitle">A premium resource for AI-Native Driven Development.</p>
        <p className="hero__subtitle">By Qaimudin Khuwaja</p>
        <div className="hero__buttons">
          <a href="/docs/intro" className="button button--secondary button--lg">
            Start Reading
          </a>
        </div>
      </div>
    </div>
  );
}

export default HomeHero;