import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Badge } from '../ui/badge';
import { toast } from 'sonner';
import { Hash, TrendingUp, Copy } from 'lucide-react';

const HashtagRecommender = () => {
  const { token, API } = useAuth();
  const [content, setContent] = useState('');
  const [platform, setPlatform] = useState('general');
  const [count, setCount] = useState(10);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRecommend = async () => {
    if (!content.trim()) {
      toast.error('Please enter your content');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${API}/marketing/hashtag-recommender`,
        { content, platform, count },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      toast.success('Hashtags generated!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate hashtags');
    } finally {
      setLoading(false);
    }
  };

  const copyAllHashtags = () => {
    if (result) {
      const tags = result.hashtags.map(h => h.tag).join(' ');
      navigator.clipboard.writeText(tags);
      toast.success('Copied all hashtags!');
    }
  };

  const getPopularityColor = (popularity) => {
    switch (popularity) {
      case 'high': return 'bg-green-100 text-green-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'low': return 'bg-blue-100 text-blue-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="space-y-6" data-testid="hashtag-recommender">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Hash className="w-6 h-6 text-purple-600" />
            Hashtag Recommender
          </CardTitle>
          <CardDescription>
            Get trending, relevant hashtags to maximize your reach
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="content">Your Content</Label>
            <Textarea
              id="content"
              placeholder="Paste or describe your post content..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={4}
              data-testid="content-input"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Platform</Label>
              <Select value={platform} onValueChange={setPlatform}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="general">General</SelectItem>
                  <SelectItem value="instagram">Instagram</SelectItem>
                  <SelectItem value="twitter">Twitter</SelectItem>
                  <SelectItem value="linkedin">LinkedIn</SelectItem>
                  <SelectItem value="facebook">Facebook</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Number of Hashtags</Label>
              <Select value={count.toString()} onValueChange={(v) => setCount(parseInt(v))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="5">5 hashtags</SelectItem>
                  <SelectItem value="10">10 hashtags</SelectItem>
                  <SelectItem value="15">15 hashtags</SelectItem>
                  <SelectItem value="20">20 hashtags</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button
            onClick={handleRecommend}
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            data-testid="recommend-button"
          >
            {loading ? 'Generating...' : 'Recommend Hashtags'}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <Card data-testid="hashtag-results">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Recommended Hashtags</CardTitle>
                <CardDescription className="mt-2">{result.content_summary}</CardDescription>
              </div>
              <Button variant="outline" size="sm" onClick={copyAllHashtags}>
                <Copy className="w-4 h-4 mr-2" />
                Copy All
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-3">
              {result.hashtags.map((hashtag, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-2 bg-white border rounded-lg px-4 py-2 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => {
                    navigator.clipboard.writeText(hashtag.tag);
                    toast.success(`Copied ${hashtag.tag}`);
                  }}
                >
                  <span className="font-semibold text-purple-600">{hashtag.tag}</span>
                  <Badge className={getPopularityColor(hashtag.popularity)} variant="secondary">
                    {hashtag.popularity}
                  </Badge>
                  <span className="text-xs text-gray-500">{hashtag.relevance_score}%</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default HashtagRecommender;