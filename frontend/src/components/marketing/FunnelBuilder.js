import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Label } from '../ui/label';
import { Input } from '../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { toast } from 'sonner';
import { TrendingUp, ArrowRight } from 'lucide-react';

const FunnelBuilder = () => {
  const { token, API } = useAuth();
  const [businessType, setBusinessType] = useState('');
  const [goal, setGoal] = useState('leads');
  const [budget, setBudget] = useState('');
  const [loading, setLoading] = useState(false);
  const [funnel, setFunnel] = useState(null);

  const handleBuild = async () => {
    if (!businessType.trim()) {
      toast.error('Please enter your business type');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${API}/marketing/funnel-builder`,
        { business_type: businessType, goal, budget: budget || null },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setFunnel(response.data);
      toast.success('Funnel created successfully!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create funnel');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6" data-testid="funnel-builder">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-purple-600" />
            Marketing Funnel Builder
          </CardTitle>
          <CardDescription>
            Generate a complete marketing funnel strategy for your business
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="businessType">Business Type *</Label>
            <Input
              id="businessType"
              placeholder="e.g., SaaS, E-commerce, Consulting, Restaurant"
              value={businessType}
              onChange={(e) => setBusinessType(e.target.value)}
              data-testid="business-type-input"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Marketing Goal</Label>
              <Select value={goal} onValueChange={setGoal}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="awareness">Brand Awareness</SelectItem>
                  <SelectItem value="leads">Generate Leads</SelectItem>
                  <SelectItem value="sales">Drive Sales</SelectItem>
                  <SelectItem value="retention">Customer Retention</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="budget">Budget (Optional)</Label>
              <Input
                id="budget"
                placeholder="e.g., $5,000/month"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
              />
            </div>
          </div>

          <Button
            onClick={handleBuild}
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            data-testid="build-funnel-button"
          >
            {loading ? 'Building Funnel...' : 'Build Marketing Funnel'}
          </Button>
        </CardContent>
      </Card>

      {funnel && (
        <div className="space-y-4" data-testid="funnel-result">
          <Card>
            <CardHeader>
              <CardTitle>{funnel.funnel_name}</CardTitle>
              <CardDescription>
                Timeline: {funnel.timeline}
              </CardDescription>
            </CardHeader>
          </Card>

          <div className="relative">
            {funnel.stages.map((stage, idx) => (
              <div key={idx} className="relative">
                <Card className="mb-4">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 text-white text-sm font-bold">
                        {idx + 1}
                      </span>
                      {stage.stage}
                    </CardTitle>
                    <CardDescription>{stage.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <Label className="text-sm font-semibold">Tactics:</Label>
                        <ul className="mt-2 space-y-1">
                          {stage.tactics.map((tactic, tidx) => (
                            <li key={tidx} className="flex items-center gap-2 text-sm">
                              <span className="text-purple-600">•</span>
                              {tactic}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <Label className="text-sm font-semibold">Key Metrics:</Label>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {stage.metrics.map((metric, midx) => (
                            <span key={midx} className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs">
                              {metric}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                {idx < funnel.stages.length - 1 && (
                  <div className="flex justify-center my-2">
                    <ArrowRight className="w-6 h-6 text-gray-400" />
                  </div>
                )}
              </div>
            ))}
          </div>

          {funnel.budget_allocation && (
            <Card>
              <CardHeader>
                <CardTitle>Budget Allocation</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(funnel.budget_allocation).map(([key, value]) => (
                    <div key={key} className="flex justify-between items-center">
                      <span className="capitalize">{key}:</span>
                      <span className="font-semibold">{value}%</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

export default FunnelBuilder;