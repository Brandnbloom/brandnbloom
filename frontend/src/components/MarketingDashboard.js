import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import AutoPublisher from './marketing/AutoPublisher';
import AdTester from './marketing/AdTester';
import HashtagRecommender from './marketing/HashtagRecommender';
import FunnelBuilder from './marketing/FunnelBuilder';
import ROICalculator from './marketing/ROICalculator';
import { Sparkles, TestTube, Hash, TrendingUp, DollarSign } from 'lucide-react';

const MarketingDashboard = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 p-6" data-testid="marketing-dashboard">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
            📣 Marketing AI Suite
          </h1>
          <p className="text-gray-600">AI-powered marketing tools to grow your business</p>
        </div>

        <Tabs defaultValue="auto-publisher" className="w-full">
          <TabsList className="grid w-full grid-cols-5 mb-8">
            <TabsTrigger value="auto-publisher" data-testid="tab-auto-publisher">
              <Sparkles className="w-4 h-4 mr-2" />
              Auto Publisher
            </TabsTrigger>
            <TabsTrigger value="ad-tester" data-testid="tab-ad-tester">
              <TestTube className="w-4 h-4 mr-2" />
              Ad Tester
            </TabsTrigger>
            <TabsTrigger value="hashtags" data-testid="tab-hashtags">
              <Hash className="w-4 h-4 mr-2" />
              Hashtags
            </TabsTrigger>
            <TabsTrigger value="funnels" data-testid="tab-funnels">
              <TrendingUp className="w-4 h-4 mr-2" />
              Funnels
            </TabsTrigger>
            <TabsTrigger value="roi" data-testid="tab-roi">
              <DollarSign className="w-4 h-4 mr-2" />
              ROI Tracker
            </TabsTrigger>
          </TabsList>

          <TabsContent value="auto-publisher">
            <AutoPublisher />
          </TabsContent>

          <TabsContent value="ad-tester">
            <AdTester />
          </TabsContent>

          <TabsContent value="hashtags">
            <HashtagRecommender />
          </TabsContent>

          <TabsContent value="funnels">
            <FunnelBuilder />
          </TabsContent>

          <TabsContent value="roi">
            <ROICalculator />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default MarketingDashboard;