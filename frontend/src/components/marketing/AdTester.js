import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Input } from '../ui/input';
import { Progress } from '../ui/progress';
import { toast } from 'sonner';
import { TestTube, TrendingUp, TrendingDown, Lightbulb } from 'lucide-react';

const AdTester = () => {
  const { token, API } = useAuth();
  const [adCopy, setAdCopy] = useState('');
  const [targetAudience, setTargetAudience] = useState('');
  const [platform, setPlatform] = useState('general');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleTest = async () => {
    if (!adCopy.trim()) {
      toast.error('Please enter your ad copy');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${API}/marketing/ad-tester`,
        { ad_copy: adCopy, target_audience: targetAudience, platform },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      toast.success('Ad analyzed successfully!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to analyze ad');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Work';
  };

  return (
    <div className="space-y-6" data-testid="ad-tester">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TestTube className="w-6 h-6 text-purple-600" />
            Ad Creative Tester
          </CardTitle>
          <CardDescription>
            Test your ad copy before launch - Get instant AI-powered feedback
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="adCopy">Ad Copy *</Label>
            <Textarea
              id="adCopy"
              placeholder="Paste your ad copy here..."
              value={adCopy}
              onChange={(e) => setAdCopy(e.target.value)}
              rows={6}
              data-testid="ad-copy-input"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="audience">Target Audience (Optional)</Label>
              <Input
                id="audience"
                placeholder="e.g., Young professionals, 25-35"
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="platform">Platform (Optional)</Label>
              <Input
                id="platform"
                placeholder="e.g., Facebook, Google Ads"
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
              />
            </div>
          </div>

          <Button
            onClick={handleTest}
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            data-testid="test-ad-button"
          >
            {loading ? 'Analyzing...' : 'Test Ad Creative'}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <div className="space-y-4" data-testid="ad-results">
          <Card>
            <CardHeader>
              <CardTitle>Ad Performance Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className={`text-6xl font-bold ${getScoreColor(result.score)}`}>
                      {result.score}
                    </p>
                    <p className="text-gray-600 mt-2">{getScoreLabel(result.score)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Sentiment</p>
                    <p className="text-lg font-semibold capitalize">{result.sentiment}</p>
                  </div>
                </div>
                <Progress value={result.score} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-green-600 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  Strengths
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {result.strengths.map((strength, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-green-600 mt-1">✓</span>
                      <span className="text-sm">{strength}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-red-600 flex items-center gap-2">
                  <TrendingDown className="w-5 h-5" />
                  Weaknesses
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {result.weaknesses.map((weakness, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-red-600 mt-1">✗</span>
                      <span className="text-sm">{weakness}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-blue-600 flex items-center gap-2">
                  <Lightbulb className="w-5 h-5" />
                  Suggestions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {result.suggestions.map((suggestion, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-blue-600 mt-1">•</span>
                      <span className="text-sm">{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdTester;