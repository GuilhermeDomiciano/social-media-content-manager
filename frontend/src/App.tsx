// src/App.tsx
import React from 'react';
// Não importe App.css aqui se você decidiu esvaziá-lo ou removê-lo
// import './App.css'; // <--- Remova ou comente esta linha se ela existir

function App() {
  return (
    // Usa classes Tailwind para estilização
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-xl text-center max-w-md w-full">
        <h1 className="text-4xl font-bold text-indigo-700 mb-4">
          Tailwind Funcionando! 🎉
        </h1>
        <p className="text-gray-700 text-lg mb-6">
          Se você está vendo este texto estilizado, o Tailwind CSS foi configurado com sucesso!
        </p>
        <button
          className="
            bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4
            rounded-lg shadow-md transition duration-300 ease-in-out transform
            hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-75
          "
        >
          Botão Estilizado com Tailwind
        </button>
        <div className="mt-8 p-4 bg-purple-100 border-l-4 border-purple-500 text-purple-700">
          <p className="font-medium">
            Exemplo de Cartão:
          </p>
          <p className="text-sm">
            Este é um exemplo de bloco estilizado com classes de utilidade Tailwind.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
