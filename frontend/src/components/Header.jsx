import React from 'react';
import { FiZap } from 'react-icons/fi';

function Header() {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center gap-3">
          <FiZap className="text-3xl text-blue-600" />
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Architecture Pattern Recommender</h1>
            <p className="text-gray-600 text-sm">AI-powered tool for selecting optimal architecture patterns</p>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
