# Hyperliquid Dart SDK - Agent Integration Guide

This document provides comprehensive guidance for integrating AI agents and automated trading systems with the Hyperliquid Dart SDK.

## Table of Contents

- [Agent Architecture](#agent-architecture)
- [Authentication & Permissions](#authentication--permissions)
- [Real-Time Data Integration](#real-time-data-integration)
- [Trading Strategy Implementation](#trading-strategy-implementation)
- [Risk Management](#risk-management)
- [Performance Optimization](#performance-optimization)
- [Example Agents](#example-agents)

## Agent Architecture

### Base Agent Structure

```dart
import 'package:hyperliquid/hyperliquid.dart';

abstract class TradingAgent {
  final Hyperliquid client;
  final String name;
  final Map<String, dynamic> config;
  
  bool _isRunning = false;
  bool _isPaused = false;

  TradingAgent({
    required this.client,
    required this.name,
    required this.config,
  });

  /// Initialize the agent
  Future<void> initialize();
  
  /// Start the agent
  Future<void> start();
  
  /// Stop the agent
  Future<void> stop();
  
  /// Pause/resume the agent
  void pause() => _isPaused = true;
  void resume() => _isPaused = false;
  
  /// Main trading logic (implement in subclasses)
  Future<void> onMarketData(dynamic data);
  Future<void> onUserEvent(dynamic event);
  Future<void> onOrderUpdate(dynamic update);
  
  /// Agent status
  bool get isRunning => _isRunning;
  bool get isPaused => _isPaused;
}
```

### Agent Manager

```dart
class AgentManager {
  final List<TradingAgent> _agents = [];
  final Map<String, StreamSubscription> _subscriptions = {};
  
  void registerAgent(TradingAgent agent) {
    _agents.add(agent);
  }
  
  Future<void> startAll() async {
    for (final agent in _agents) {
      await agent.start();
    }
  }
  
  Future<void> stopAll() async {
    for (final agent in _agents) {
      await agent.stop();
    }
    
    // Cancel all subscriptions
    for (final subscription in _subscriptions.values) {
      await subscription.cancel();
    }
    _subscriptions.clear();
  }
  
  void pauseAll() {
    for (final agent in _agents) {
      agent.pause();
    }
  }
  
  void resumeAll() {
    for (final agent in _agents) {
      agent.resume();
    }
  }
}
```

## Authentication & Permissions

### Agent Approval Process

```dart
class AgentApprovalManager {
  final Hyperliquid client;
  
  AgentApprovalManager(this.client);
  
  /// Approve an agent for trading
  Future<dynamic> approveAgent(String agentAddress, String agentName) async {
    return await client.exchange.approveAgent({
      'agentAddress': agentAddress,
      'agentName': agentName,
    });
  }
  
  /// Approve builder fees
  Future<dynamic> approveBuilderFee(String builderAddress, String maxFeeRate) async {
    return await client.exchange.approveBuilderFee({
      'builder': builderAddress,
      'maxFeeRate': maxFeeRate,
    });
  }
  
  /// Check agent approval status
  Future<bool> isAgentApproved(String agentAddress) async {
    try {
      final extraAgents = await client.info.generalAPI.extraAgents(
        client.walletAddress ?? '',
      );
      
      if (extraAgents is List) {
        return extraAgents.any((agent) => agent['address'] == agentAddress);
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}
```

## Real-Time Data Integration

### Market Data Agent

```dart
class MarketDataAgent extends TradingAgent {
  final Set<String> _watchedSymbols;
  final Map<String, dynamic> _latestPrices = {};
  final Map<String, List<dynamic>> _recentTrades = {};
  
  MarketDataAgent({
    required super.client,
    required super.name,
    required super.config,
    required Set<String> watchedSymbols,
  }) : _watchedSymbols = watchedSymbols;
  
  @override
  Future<void> initialize() async {
    await client.connect();
    
    // Subscribe to all mids for price updates
    await client.webSocket.subscriptions.subscribeToAllMids(onMarketData);
    
    // Subscribe to trades for each watched symbol
    for (final symbol in _watchedSymbols) {
      await client.webSocket.subscriptions.subscribeToTrades(symbol, onTradeData);
      await client.webSocket.subscriptions.subscribeToL2Book(symbol, onOrderBookData);
    }
  }
  
  @override
  Future<void> start() async {
    _isRunning = true;
    print('$name: Market data agent started');
  }
  
  @override
  Future<void> stop() async {
    _isRunning = false;
    await client.webSocket.subscriptions.unsubscribeAll();
    print('$name: Market data agent stopped');
  }
  
  @override
  Future<void> onMarketData(dynamic data) async {
    if (_isPaused) return;
    
    final mids = data['mids'] as Map<String, dynamic>?;
    if (mids != null) {
      _latestPrices.addAll(mids);
      await _analyzeMarketMovement();
    }
  }
  
  Future<void> onTradeData(dynamic data) async {
    if (_isPaused) return;
    
    final trades = data as List<dynamic>?;
    if (trades != null) {
      for (final trade in trades) {
        final coin = trade['coin'] as String?;
        if (coin != null && _watchedSymbols.contains(coin)) {
          _recentTrades.putIfAbsent(coin, () => []).add(trade);
          
          // Keep only last 100 trades per symbol
          if (_recentTrades[coin]!.length > 100) {
            _recentTrades[coin]!.removeAt(0);
          }
        }
      }
    }
  }
  
  Future<void> onOrderBookData(dynamic data) async {
    if (_isPaused) return;
    
    // Process order book updates
    await _analyzeOrderBookImbalance(data);
  }
  
  Future<void> _analyzeMarketMovement() async {
    // Implement market movement analysis
    for (final symbol in _watchedSymbols) {
      final currentPrice = _latestPrices[symbol];
      if (currentPrice != null) {
        // Add your analysis logic here
        print('$symbol: Current price = $currentPrice');
      }
    }
  }
  
  Future<void> _analyzeOrderBookImbalance(dynamic orderBook) async {
    // Implement order book analysis
    final levels = orderBook['levels'] as List<dynamic>?;
    if (levels != null && levels.length >= 2) {
      final bids = levels[0] as List<dynamic>;
      final asks = levels[1] as List<dynamic>;
      
      // Calculate bid/ask imbalance
      if (bids.isNotEmpty && asks.isNotEmpty) {
        final bidVolume = bids.fold<double>(0.0, (sum, bid) => sum + double.parse(bid[1].toString()));
        final askVolume = asks.fold<double>(0.0, (sum, ask) => sum + double.parse(ask[1].toString()));
        final imbalance = (bidVolume - askVolume) / (bidVolume + askVolume);
        
        print('Order book imbalance: ${(imbalance * 100).toStringAsFixed(2)}%');
      }
    }
  }
  
  @override
  Future<void> onUserEvent(dynamic event) async {
    // Handle user-specific events if needed
  }
  
  @override
  Future<void> onOrderUpdate(dynamic update) async {
    // Handle order updates if needed
  }
  
  // Getters for other agents to access market data
  Map<String, dynamic> get latestPrices => Map.from(_latestPrices);
  Map<String, List<dynamic>> get recentTrades => Map.from(_recentTrades);
}
```

## Trading Strategy Implementation

### Momentum Trading Agent

```dart
class MomentumTradingAgent extends TradingAgent {
  final MarketDataAgent marketDataAgent;
  final double priceChangeThreshold;
  final double positionSize;
  final Duration lookbackPeriod;
  
  final Map<String, List<PricePoint>> _priceHistory = {};
  final Map<String, DateTime> _lastTradeTime = {};
  final Duration _minTimeBetweenTrades;
  
  MomentumTradingAgent({
    required super.client,
    required super.name,
    required super.config,
    required this.marketDataAgent,
    this.priceChangeThreshold = 0.02, // 2%
    this.positionSize = 0.001,
    this.lookbackPeriod = const Duration(minutes: 15),
    Duration? minTimeBetweenTrades,
  }) : _minTimeBetweenTrades = minTimeBetweenTrades ?? const Duration(minutes: 5);
  
  @override
  Future<void> initialize() async {
    await client.connect();
    
    // Subscribe to user order updates
    if (client.walletAddress != null) {
      await client.webSocket.subscriptions.subscribeToOrderUpdates(
        client.walletAddress!, 
        onOrderUpdate,
      );
    }
  }
  
  @override
  Future<void> start() async {
    _isRunning = true;
    
    // Start monitoring market data
    _startPriceMonitoring();
    
    print('$name: Momentum trading agent started');
  }
  
  @override
  Future<void> stop() async {
    _isRunning = false;
    print('$name: Momentum trading agent stopped');
  }
  
  void _startPriceMonitoring() {
    Timer.periodic(const Duration(seconds: 30), (timer) async {
      if (!_isRunning || _isPaused) return;
      
      await _checkMomentumSignals();
    });
  }
  
  Future<void> _checkMomentumSignals() async {
    final currentPrices = marketDataAgent.latestPrices;
    final now = DateTime.now();
    
    for (final entry in currentPrices.entries) {
      final symbol = entry.key;
      final currentPrice = double.tryParse(entry.value.toString());
      
      if (currentPrice == null) continue;
      
      // Update price history
      _priceHistory.putIfAbsent(symbol, () => []).add(
        PricePoint(price: currentPrice, timestamp: now),
      );
      
      // Remove old price points
      _priceHistory[symbol]!.removeWhere(
        (point) => now.difference(point.timestamp) > lookbackPeriod,
      );
      
      // Check for momentum signals
      await _evaluateMomentumSignal(symbol, currentPrice);
    }
  }
  
  Future<void> _evaluateMomentumSignal(String symbol, double currentPrice) async {
    final priceHistory = _priceHistory[symbol];
    if (priceHistory == null || priceHistory.length < 2) return;
    
    // Check minimum time between trades
    final lastTrade = _lastTradeTime[symbol];
    if (lastTrade != null && DateTime.now().difference(lastTrade) < _minTimeBetweenTrades) {
      return;
    }
    
    // Calculate price change over lookback period
    final oldestPrice = priceHistory.first.price;
    final priceChange = (currentPrice - oldestPrice) / oldestPrice;
    
    // Generate signals
    if (priceChange.abs() > priceChangeThreshold) {
      final isUptrend = priceChange > 0;
      await _executeTradeSignal(symbol, isUptrend, currentPrice);
    }
  }
  
  Future<void> _executeTradeSignal(String symbol, bool isBuy, double currentPrice) async {
    try {
      // Check current position
      final position = await client.customOperations.getPosition(symbol);
      final hasPosition = position != null && double.parse(position['szi'].toString()) != 0;
      
      if (hasPosition) {
        // Close existing position if direction changed
        final currentPositionSide = double.parse(position!['szi'].toString()) > 0;
        if (currentPositionSide != isBuy) {
          await client.customOperations.marketClose(symbol, slippage: 0.01);
          print('$name: Closed ${hasPosition ? 'opposing' : 'existing'} position in $symbol');
        }
      }
      
      // Open new position
      final response = await client.customOperations.marketOpen(
        symbol,
        isBuy,
        positionSize,
        slippage: 0.01,
      );
      
      _lastTradeTime[symbol] = DateTime.now();
      
      print('$name: ${isBuy ? 'BOUGHT' : 'SOLD'} $positionSize $symbol at ~$currentPrice');
      print('Trade response: $response');
      
    } catch (e) {
      print('$name: Error executing trade for $symbol: $e');
    }
  }
  
  @override
  Future<void> onMarketData(dynamic data) async {
    // Market data is handled by the MarketDataAgent
  }
  
  @override
  Future<void> onUserEvent(dynamic event) async {
    print('$name: User event received: $event');
  }
  
  @override
  Future<void> onOrderUpdate(dynamic update) async {
    print('$name: Order update: $update');
  }
}

class PricePoint {
  final double price;
  final DateTime timestamp;
  
  PricePoint({required this.price, required this.timestamp});
}
```

### Grid Trading Agent

```dart
class GridTradingAgent extends TradingAgent {
  final String symbol;
  final double gridSpacing;
  final int numberOfGrids;
  final double orderSize;
  final double centerPrice;
  
  final List<GridOrder> _gridOrders = [];
  
  GridTradingAgent({
    required super.client,
    required super.name,
    required super.config,
    required this.symbol,
    required this.gridSpacing,
    required this.numberOfGrids,
    required this.orderSize,
    required this.centerPrice,
  });
  
  @override
  Future<void> initialize() async {
    await client.connect();
    
    // Subscribe to order updates and fills
    if (client.walletAddress != null) {
      await client.webSocket.subscriptions.subscribeToOrderUpdates(
        client.walletAddress!,
        onOrderUpdate,
      );
      
      await client.webSocket.subscriptions.subscribeToUserFills(
        client.walletAddress!,
        _onFill,
      );
    }
  }
  
  @override
  Future<void> start() async {
    _isRunning = true;
    await _setupGridOrders();
    print('$name: Grid trading agent started for $symbol');
  }
  
  @override
  Future<void> stop() async {
    _isRunning = false;
    await _cancelAllGridOrders();
    print('$name: Grid trading agent stopped');
  }
  
  Future<void> _setupGridOrders() async {
    try {
      // Create buy orders below center price
      for (int i = 1; i <= numberOfGrids ~/ 2; i++) {
        final price = centerPrice - (i * gridSpacing);
        final orderId = await _placeBuyOrder(price);
        _gridOrders.add(GridOrder(
          orderId: orderId,
          price: price,
          isBuy: true,
          size: orderSize,
        ));
      }
      
      // Create sell orders above center price
      for (int i = 1; i <= numberOfGrids ~/ 2; i++) {
        final price = centerPrice + (i * gridSpacing);
        final orderId = await _placeSellOrder(price);
        _gridOrders.add(GridOrder(
          orderId: orderId,
          price: price,
          isBuy: false,
          size: orderSize,
        ));
      }
      
      print('$name: Set up ${_gridOrders.length} grid orders');
      
    } catch (e) {
      print('$name: Error setting up grid orders: $e');
    }
  }
  
  Future<String> _placeBuyOrder(double price) async {
    final response = await client.exchange.placeOrder({
      'coin': symbol,
      'is_buy': true,
      'sz': orderSize,
      'px': price,
      'order_type': {'limit': {'tif': 'Gtc'}},
      'reduce_only': false,
    });
    
    // Extract order ID from response
    return response['response']['data']['statuses'][0]['resting']['oid'].toString();
  }
  
  Future<String> _placeSellOrder(double price) async {
    final response = await client.exchange.placeOrder({
      'coin': symbol,
      'is_buy': false,
      'sz': orderSize,
      'px': price,
      'order_type': {'limit': {'tif': 'Gtc'}},
      'reduce_only': false,
    });
    
    // Extract order ID from response
    return response['response']['data']['statuses'][0]['resting']['oid'].toString();
  }
  
  Future<void> _onFill(dynamic fillData) async {
    if (_isPaused || !_isRunning) return;
    
    final fills = fillData as List<dynamic>?;
    if (fills == null) return;
    
    for (final fill in fills) {
      final coin = fill['coin'] as String?;
      final orderId = fill['oid'] as int?;
      
      if (coin == symbol && orderId != null) {
        await _handleGridOrderFill(orderId.toString(), fill);
      }
    }
  }
  
  Future<void> _handleGridOrderFill(String orderId, dynamic fillData) async {
    // Find the filled grid order
    final gridOrderIndex = _gridOrders.indexWhere((order) => order.orderId == orderId);
    if (gridOrderIndex == -1) return;
    
    final filledOrder = _gridOrders[gridOrderIndex];
    _gridOrders.removeAt(gridOrderIndex);
    
    print('$name: Grid order filled - ${filledOrder.isBuy ? 'BUY' : 'SELL'} at ${filledOrder.price}');
    
    // Place opposite order at the same price level
    try {
      final newOrderId = filledOrder.isBuy
          ? await _placeSellOrder(filledOrder.price + gridSpacing)
          : await _placeBuyOrder(filledOrder.price - gridSpacing);
      
      _gridOrders.add(GridOrder(
        orderId: newOrderId,
        price: filledOrder.isBuy ? filledOrder.price + gridSpacing : filledOrder.price - gridSpacing,
        isBuy: !filledOrder.isBuy,
        size: orderSize,
      ));
      
      print('$name: Placed new grid order at ${filledOrder.isBuy ? filledOrder.price + gridSpacing : filledOrder.price - gridSpacing}');
      
    } catch (e) {
      print('$name: Error placing replacement grid order: $e');
    }
  }
  
  Future<void> _cancelAllGridOrders() async {
    for (final gridOrder in _gridOrders) {
      try {
        await client.exchange.cancelOrder({
          'coin': symbol,
          'o': int.parse(gridOrder.orderId),
        });
      } catch (e) {
        print('$name: Error cancelling order ${gridOrder.orderId}: $e');
      }
    }
    _gridOrders.clear();
  }
  
  @override
  Future<void> onMarketData(dynamic data) async {
    // Monitor market data for grid adjustments if needed
  }
  
  @override
  Future<void> onUserEvent(dynamic event) async {
    // Handle user events
  }
  
  @override
  Future<void> onOrderUpdate(dynamic update) async {
    // Handle order status changes
  }
}

class GridOrder {
  final String orderId;
  final double price;
  final bool isBuy;
  final double size;
  
  GridOrder({
    required this.orderId,
    required this.price,
    required this.isBuy,
    required this.size,
  });
}
```

## Risk Management

### Risk Management Agent

```dart
class RiskManagementAgent extends TradingAgent {
  final double maxDrawdown;
  final double maxPositionSize;
  final double maxDailyLoss;
  final Map<String, double> positionLimits;
  
  double _initialEquity = 0;
  double _dailyStartEquity = 0;
  DateTime _lastEquityReset = DateTime.now();
  
  RiskManagementAgent({
    required super.client,
    required super.name,
    required super.config,
    required this.maxDrawdown,
    required this.maxPositionSize,
    required this.maxDailyLoss,
    required this.positionLimits,
  });
  
  @override
  Future<void> initialize() async {
    await client.connect();
    
    // Get initial account equity
    _initialEquity = await client.customOperations.getAccountEquity();
    _dailyStartEquity = _initialEquity;
    
    // Subscribe to user events for real-time monitoring
    if (client.walletAddress != null) {
      await client.webSocket.subscriptions.subscribeToUserEvents(
        client.walletAddress!,
        onUserEvent,
      );
    }
  }
  
  @override
  Future<void> start() async {
    _isRunning = true;
    
    // Start periodic risk checks
    Timer.periodic(const Duration(seconds: 30), (timer) async {
      if (!_isRunning || _isPaused) return;
      await _performRiskChecks();
    });
    
    print('$name: Risk management agent started');
  }
  
  @override
  Future<void> stop() async {
    _isRunning = false;
    print('$name: Risk management agent stopped');
  }
  
  Future<void> _performRiskChecks() async {
    try {
      // Reset daily tracking if new day
      final now = DateTime.now();
      if (now.day != _lastEquityReset.day) {
        _dailyStartEquity = await client.customOperations.getAccountEquity();
        _lastEquityReset = now;
      }
      
      final currentEquity = await client.customOperations.getAccountEquity();
      final unrealizedPnL = await client.customOperations.getUnrealizedPnL();
      
      // Check maximum drawdown
      final drawdown = (_initialEquity - currentEquity) / _initialEquity;
      if (drawdown > maxDrawdown) {
        await _handleMaxDrawdownBreach(drawdown);
      }
      
      // Check daily loss limit
      final dailyPnL = currentEquity - _dailyStartEquity;
      if (dailyPnL < -maxDailyLoss) {
        await _handleDailyLossLimitBreach(dailyPnL);
      }
      
      // Check position size limits
      await _checkPositionSizes();
      
      print('$name: Risk check - Equity: \$${currentEquity.toStringAsFixed(2)}, '
            'Drawdown: ${(drawdown * 100).toStringAsFixed(2)}%, '
            'Daily PnL: \$${dailyPnL.toStringAsFixed(2)}');
      
    } catch (e) {
      print('$name: Error performing risk checks: $e');
    }
  }
  
  Future<void> _handleMaxDrawdownBreach(double drawdown) async {
    print('$name: RISK ALERT - Maximum drawdown breached: ${(drawdown * 100).toStringAsFixed(2)}%');
    
    // Close all positions
    try {
      await client.customOperations.closeAllPositions(slippage: 0.02);
      print('$name: Emergency position closure due to max drawdown breach');
    } catch (e) {
      print('$name: Error closing positions during risk management: $e');
    }
    
    // Pause all other agents
    // Note: In a real implementation, you'd need a reference to the AgentManager
    print('$name: Consider pausing all trading agents');
  }
  
  Future<void> _handleDailyLossLimitBreach(double dailyPnL) async {
    print('$name: RISK ALERT - Daily loss limit breached: \$${dailyPnL.toStringAsFixed(2)}');
    
    // Close all positions
    await client.customOperations.closeAllPositions(slippage: 0.02);
    
    // Cancel all open orders
    await client.customOperations.cancelAllOrders();
    
    print('$name: Trading halted due to daily loss limit breach');
  }
  
  Future<void> _checkPositionSizes() async {
    final positions = await client.customOperations.getAllPositions();
    
    for (final position in positions) {
      final symbol = position['userSymbol'] as String;
      final size = double.parse(position['szi'].toString()).abs();
      
      // Check against maximum position size
      if (size > maxPositionSize) {
        await _reducePositionSize(symbol, size);
      }
      
      // Check against symbol-specific limits
      final symbolLimit = positionLimits[symbol];
      if (symbolLimit != null && size > symbolLimit) {
        await _reducePositionSize(symbol, size);
      }
    }
  }
  
  Future<void> _reducePositionSize(String symbol, double currentSize) async {
    print('$name: RISK ALERT - Position size too large for $symbol: ${currentSize.toStringAsFixed(6)}');
    
    try {
      // Reduce position to maximum allowed size
      final maxAllowed = positionLimits[symbol] ?? maxPositionSize;
      final excessSize = currentSize - maxAllowed;
      
      await client.customOperations.marketClose(
        symbol,
        size: excessSize,
        slippage: 0.01,
      );
      
      print('$name: Reduced $symbol position by ${excessSize.toStringAsFixed(6)}');
      
    } catch (e) {
      print('$name: Error reducing position size for $symbol: $e');
    }
  }
  
  @override
  Future<void> onMarketData(dynamic data) async {
    // Monitor market data for risk-related signals
  }
  
  @override
  Future<void> onUserEvent(dynamic event) async {
    // Handle user events that might affect risk
    print('$name: User event: $event');
  }
  
  @override
  Future<void> onOrderUpdate(dynamic update) async {
    // Monitor order updates for risk assessment
  }
  
  /// Check if a trade is allowed based on risk parameters
  Future<bool> isTradeAllowed(String symbol, double size, bool isBuy) async {
    try {
      // Check current position
      final position = await client.customOperations.getPosition(symbol);
      double currentSize = 0;
      
      if (position != null) {
        currentSize = double.parse(position['szi'].toString()).abs();
      }
      
      final newSize = currentSize + size;
      
      // Check position size limits
      if (newSize > maxPositionSize) return false;
      
      final symbolLimit = positionLimits[symbol];
      if (symbolLimit != null && newSize > symbolLimit) return false;
      
      // Check daily loss limit
      final currentEquity = await client.customOperations.getAccountEquity();
      final dailyPnL = currentEquity - _dailyStartEquity;
      if (dailyPnL < -maxDailyLoss * 0.8) { // 80% of daily limit
        return false;
      }
      
      return true;
      
    } catch (e) {
      print('$name: Error checking trade allowance: $e');
      return false; // Err on the side of caution
    }
  }
}
```

## Performance Optimization

### Performance Monitoring Agent

```dart
class PerformanceMonitoringAgent extends TradingAgent {
  final Map<String, PerformanceMetrics> _symbolMetrics = {};
  final List<Trade> _tradeHistory = [];
  final Duration _reportingInterval;
  
  Timer? _reportingTimer;
  
  PerformanceMonitoringAgent({
    required super.client,
    required super.name,
    required super.config,
    Duration? reportingInterval,
  }) : _reportingInterval = reportingInterval ?? const Duration(hours: 1);
  
  @override
  Future<void> initialize() async {
    await client.connect();
    
    if (client.walletAddress != null) {
      await client.webSocket.subscriptions.subscribeToUserFills(
        client.walletAddress!,
        _onFill,
      );
    }
  }
  
  @override
  Future<void> start() async {
    _isRunning = true;
    
    _reportingTimer = Timer.periodic(_reportingInterval, (timer) async {
      if (_isRunning && !_isPaused) {
        await _generatePerformanceReport();
      }
    });
    
    print('$name: Performance monitoring agent started');
  }
  
  @override
  Future<void> stop() async {
    _isRunning = false;
    _reportingTimer?.cancel();
    print('$name: Performance monitoring agent stopped');
  }
  
  Future<void> _onFill(dynamic fillData) async {
    final fills = fillData as List<dynamic>?;
    if (fills == null) return;
    
    for (final fill in fills) {
      final trade = Trade(
        symbol: fill['coin'] as String,
        side: fill['side'] as String,
        size: double.parse(fill['sz'].toString()),
        price: double.parse(fill['px'].toString()),
        timestamp: DateTime.fromMillisecondsSinceEpoch(fill['time'] as int),
        fee: double.parse(fill['fee'].toString()),
      );
      
      _tradeHistory.add(trade);
      _updateMetrics(trade);
    }
  }
  
  void _updateMetrics(Trade trade) {
    final metrics = _symbolMetrics.putIfAbsent(
      trade.symbol,
      () => PerformanceMetrics(symbol: trade.symbol),
    );
    
    metrics.addTrade(trade);
  }
  
  Future<void> _generatePerformanceReport() async {
    print('\n$name: PERFORMANCE REPORT');
    print('=' * 50);
    
    // Overall statistics
    final totalTrades = _tradeHistory.length;
    final totalVolume = _tradeHistory.fold<double>(0, (sum, trade) => sum + trade.notional);
    final totalFees = _tradeHistory.fold<double>(0, (sum, trade) => sum + trade.fee);
    
    print('Total Trades: $totalTrades');
    print('Total Volume: \$${totalVolume.toStringAsFixed(2)}');
    print('Total Fees: \$${totalFees.toStringAsFixed(2)}');
    
    // Account metrics
    try {
      final equity = await client.customOperations.getAccountEquity();
      final unrealizedPnL = await client.customOperations.getUnrealizedPnL();
      
      print('Account Equity: \$${equity.toStringAsFixed(2)}');
      print('Unrealized PnL: \$${unrealizedPnL.toStringAsFixed(2)}');
    } catch (e) {
      print('Error fetching account metrics: $e');
    }
    
    // Per-symbol breakdown
    print('\nPer-Symbol Performance:');
    for (final metrics in _symbolMetrics.values) {
      print('${metrics.symbol}:');
      print('  Trades: ${metrics.tradeCount}');
      print('  Volume: \$${metrics.totalVolume.toStringAsFixed(2)}');
      print('  Avg Trade Size: \$${metrics.averageTradeSize.toStringAsFixed(2)}');
      print('  Total Fees: \$${metrics.totalFees.toStringAsFixed(2)}');
    }
    
    // Rate limiting statistics
    final rateLimitStats = client.getRateLimitStats();
    print('\nRate Limiting:');
    print('  Total Requests: ${rateLimitStats['totalRequests']}');
    print('  Current Utilization: ${rateLimitStats['utilizationPercent']}%');
    print('  Wait Events: ${rateLimitStats['waitEvents']}');
    
    print('=' * 50);
  }
  
  @override
  Future<void> onMarketData(dynamic data) async {}
  
  @override
  Future<void> onUserEvent(dynamic event) async {}
  
  @override
  Future<void> onOrderUpdate(dynamic update) async {}
  
  /// Get performance metrics for a specific symbol
  PerformanceMetrics? getSymbolMetrics(String symbol) {
    return _symbolMetrics[symbol];
  }
  
  /// Get all trade history
  List<Trade> get tradeHistory => List.from(_tradeHistory);
}

class Trade {
  final String symbol;
  final String side;
  final double size;
  final double price;
  final DateTime timestamp;
  final double fee;
  
  Trade({
    required this.symbol,
    required this.side,
    required this.size,
    required this.price,
    required this.timestamp,
    required this.fee,
  });
  
  double get notional => size * price;
}

class PerformanceMetrics {
  final String symbol;
  final List<Trade> _trades = [];
  
  PerformanceMetrics({required this.symbol});
  
  void addTrade(Trade trade) {
    _trades.add(trade);
  }
  
  int get tradeCount => _trades.length;
  
  double get totalVolume => _trades.fold(0, (sum, trade) => sum + trade.notional);
  
  double get totalFees => _trades.fold(0, (sum, trade) => sum + trade.fee);
  
  double get averageTradeSize => tradeCount > 0 ? totalVolume / tradeCount : 0;
  
  List<Trade> get trades => List.from(_trades);
}
```

## Example Agents

### Complete Agent Setup Example

```dart
Future<void> main() async {
  // Initialize Hyperliquid client
  final client = Hyperliquid(const HyperliquidConfig(
    testnet: true,
    enableWs: true,
    privateKey: '0xYOUR_PRIVATE_KEY',
  ));
  
  await client.connect();
  
  // Create agent manager
  final agentManager = AgentManager();
  
  // Create market data agent
  final marketDataAgent = MarketDataAgent(
    client: client,
    name: 'MarketDataAgent',
    config: {},
    watchedSymbols: {'BTC', 'ETH', 'SOL'},
  );
  
  // Create momentum trading agent
  final momentumAgent = MomentumTradingAgent(
    client: client,
    name: 'MomentumTrader',
    config: {},
    marketDataAgent: marketDataAgent,
    priceChangeThreshold: 0.015, // 1.5%
    positionSize: 0.001,
  );
  
  // Create grid trading agent
  final gridAgent = GridTradingAgent(
    client: client,
    name: 'GridTrader',
    config: {},
    symbol: 'BTC',
    gridSpacing: 100.0, // $100 spacing
    numberOfGrids: 10,
    orderSize: 0.001,
    centerPrice: 50000.0,
  );
  
  // Create risk management agent
  final riskAgent = RiskManagementAgent(
    client: client,
    name: 'RiskManager',
    config: {},
    maxDrawdown: 0.10, // 10%
    maxPositionSize: 0.01,
    maxDailyLoss: 500.0, // $500
    positionLimits: {
      'BTC': 0.005,
      'ETH': 0.05,
      'SOL': 5.0,
    },
  );
  
  // Create performance monitoring agent
  final performanceAgent = PerformanceMonitoringAgent(
    client: client,
    name: 'PerformanceMonitor',
    config: {},
    reportingInterval: const Duration(minutes: 30),
  );
  
  // Register all agents
  agentManager.registerAgent(marketDataAgent);
  agentManager.registerAgent(momentumAgent);
  agentManager.registerAgent(gridAgent);
  agentManager.registerAgent(riskAgent);
  agentManager.registerAgent(performanceAgent);
  
  // Initialize all agents
  for (final agent in [marketDataAgent, momentumAgent, gridAgent, riskAgent, performanceAgent]) {
    await agent.initialize();
  }
  
  // Start all agents
  await agentManager.startAll();
  
  print('All agents started successfully!');
  
  // Handle shutdown gracefully
  ProcessSignal.sigint.watch().listen((signal) async {
    print('Shutting down agents...');
    await agentManager.stopAll();
    await client.disconnect();
    exit(0);
  });
  
  // Keep the program running
  while (true) {
    await Future.delayed(const Duration(seconds: 10));
    
    // Optional: Print agent status
    print('Agents running... (press Ctrl+C to stop)');
  }
}
```

### Simple Trading Bot Example

```dart
class SimpleTradingBot extends TradingAgent {
  final String targetSymbol;
  final double buyThreshold;
  final double sellThreshold;
  final double orderSize;
  
  double? _lastPrice;
  bool _hasPosition = false;
  
  SimpleTradingBot({
    required super.client,
    required super.name,
    required super.config,
    required this.targetSymbol,
    required this.buyThreshold,
    required this.sellThreshold,
    required this.orderSize,
  });
  
  @override
  Future<void> initialize() async {
    await client.connect();
    
    // Subscribe to price updates for our target symbol
    await client.webSocket.subscriptions.subscribeToAllMids(onMarketData);
  }
  
  @override
  Future<void> start() async {
    _isRunning = true;
    print('$name: Simple trading bot started for $targetSymbol');
  }
  
  @override
  Future<void> stop() async {
    _isRunning = false;
    print('$name: Simple trading bot stopped');
  }
  
  @override
  Future<void> onMarketData(dynamic data) async {
    if (_isPaused || !_isRunning) return;
    
    final mids = data['mids'] as Map<String, dynamic>?;
    if (mids == null) return;
    
    final currentPriceStr = mids[targetSymbol]?.toString();
    if (currentPriceStr == null) return;
    
    final currentPrice = double.tryParse(currentPriceStr);
    if (currentPrice == null) return;
    
    if (_lastPrice != null) {
      final priceChange = (currentPrice - _lastPrice!) / _lastPrice!;
      
      // Buy signal: price dropped by buyThreshold
      if (!_hasPosition && priceChange <= -buyThreshold) {
        await _executeBuy(currentPrice);
      }
      
      // Sell signal: price increased by sellThreshold (and we have position)
      if (_hasPosition && priceChange >= sellThreshold) {
        await _executeSell(currentPrice);
      }
    }
    
    _lastPrice = currentPrice;
  }
  
  Future<void> _executeBuy(double price) async {
    try {
      final response = await client.customOperations.marketOpen(
        targetSymbol,
        true,
        orderSize,
        slippage: 0.01,
      );
      
      _hasPosition = true;
      print('$name: BOUGHT $orderSize $targetSymbol at ~\$${price.toStringAsFixed(2)}');
      
    } catch (e) {
      print('$name: Error executing buy: $e');
    }
  }
  
  Future<void> _executeSell(double price) async {
    try {
      final response = await client.customOperations.marketClose(
        targetSymbol,
        slippage: 0.01,
      );
      
      _hasPosition = false;
      print('$name: SOLD $targetSymbol position at ~\$${price.toStringAsFixed(2)}');
      
    } catch (e) {
      print('$name: Error executing sell: $e');
    }
  }
  
  @override
  Future<void> onUserEvent(dynamic event) async {}
  
  @override
  Future<void> onOrderUpdate(dynamic update) async {}
}

// Usage:
Future<void> runSimpleBot() async {
  final client = Hyperliquid(const HyperliquidConfig(
    testnet: true,
    enableWs: true,
    privateKey: '0xYOUR_PRIVATE_KEY',
  ));
  
  final bot = SimpleTradingBot(
    client: client,
    name: 'SimpleBot',
    config: {},
    targetSymbol: 'BTC',
    buyThreshold: 0.02, // Buy on 2% dip
    sellThreshold: 0.03, // Sell on 3% rise
    orderSize: 0.001,
  );
  
  await bot.initialize();
  await bot.start();
  
  // Keep running
  while (true) {
    await Future.delayed(const Duration(seconds: 1));
  }
}
```

## Best Practices

### Error Handling

```dart
class RobustAgent extends TradingAgent {
  int _consecutiveErrors = 0;
  static const int maxConsecutiveErrors = 5;
  
  @override
  Future<void> onMarketData(dynamic data) async {
    try {
      // Your trading logic here
      await _processMarketData(data);
      
      // Reset error counter on success
      _consecutiveErrors = 0;
      
    } catch (e) {
      _consecutiveErrors++;
      print('$name: Error processing market data: $e (${_consecutiveErrors}/${maxConsecutiveErrors})');
      
      if (_consecutiveErrors >= maxConsecutiveErrors) {
        print('$name: Too many consecutive errors, pausing agent');
        pause();
        
        // Optionally, attempt recovery after a delay
        Timer(const Duration(minutes: 5), () {
          print('$name: Attempting to resume after error recovery period');
          resume();
          _consecutiveErrors = 0;
        });
      }
    }
  }
  
  Future<void> _processMarketData(dynamic data) async {
    // Implement your market data processing logic
  }
  
  // ... other required methods
}
```

### Logging and Monitoring

```dart
import 'package:logger/logger.dart';

class LoggedAgent extends TradingAgent {
  final Logger _logger = Logger(
    printer: PrettyPrinter(
      methodCount: 2,
      errorMethodCount: 8,
      lineLength: 120,
      colors: true,
      printEmojis: true,
      printTime: true,
    ),
  );
  
  @override
  Future<void> start() async {
    _isRunning = true;
    _logger.i('$name: Agent started successfully');
  }
  
  @override
  Future<void> onMarketData(dynamic data) async {
    _logger.d('$name: Received market data update');
    
    try {
      // Process data
      await _processData(data);
      
    } catch (e, stackTrace) {
      _logger.e('$name: Error processing market data', e, stackTrace);
    }
  }
  
  Future<void> _processData(dynamic data) async {
    // Implementation
  }
  
  // ... other methods
}
```

This comprehensive guide provides the foundation for building sophisticated trading agents with the Hyperliquid Dart SDK. Remember to always test thoroughly on testnet before deploying to mainnet, and implement proper risk management and error handling in all production agents.