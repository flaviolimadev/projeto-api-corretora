// Teste simples do gráfico
function testChart() {
    console.log('🧪 Testando gráfico...');
    
    // Dados de teste
    const testData = [
        { time: 1640995200, open: 47000, high: 48000, low: 46000, close: 47500 },
        { time: 1640995260, open: 47500, high: 48500, low: 47000, close: 48000 },
        { time: 1640995320, open: 48000, high: 49000, low: 47500, close: 48500 },
        { time: 1640995380, open: 48500, high: 49500, low: 48000, close: 49000 },
        { time: 1640995440, open: 49000, high: 50000, low: 48500, close: 49500 },
    ];
    
    // Verificar se o gráfico existe
    if (typeof chart === 'undefined') {
        console.error('❌ Gráfico não encontrado');
        return;
    }
    
    if (typeof candlestickSeries === 'undefined') {
        console.error('❌ Série de candlesticks não encontrada');
        return;
    }
    
    console.log('✅ Gráfico e série encontrados');
    console.log('📊 Adicionando dados de teste...');
    
    try {
        candlestickSeries.setData(testData);
        console.log('✅ Dados de teste adicionados com sucesso!');
    } catch (error) {
        console.error('❌ Erro ao adicionar dados:', error);
    }
}

// Executar teste após 2 segundos
setTimeout(testChart, 2000);
