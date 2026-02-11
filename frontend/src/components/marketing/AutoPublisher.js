import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { toast } from 'sonner';
import { Sparkles, Copy, Check } from 'lucide-react';

const AutoPublisher = () => {
  const { token, API } = useAuth();
  const [topic, setTopic] = useState('');
  const [platform, setPlatform] = useState('social_media');
  const [tone, setTone] = useState('professional');
  const [length, setLength] = useState('medium');
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async () => {
    if (!topic.trim()) {
      toast.error('Please enter a topic');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${API}/marketing/content-generator`,
        { topic, platform, tone, length },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setGeneratedContent(response.data);
      toast.success('Content generated successfully!');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate content');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (generatedContent) {
      navigator.clipboard.writeText(generatedContent.content);
      setCopied(true);
      toast.success('Copied to clipboard!');
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className=\"space-y-6\" data-testid=\"auto-publisher\">
      <Card>
        <CardHeader>
          <CardTitle className=\"flex items-center gap-2\">
            <Sparkles className=\"w-6 h-6 text-purple-600\" />
            AI Content Generator
          </CardTitle>
          <CardDescription>
            Generate engaging marketing content for any platform in seconds
          </CardDescription>
        </CardHeader>
        <CardContent className=\"space-y-4\">
          <div className=\"space-y-2\">
            <Label htmlFor=\"topic\">What's your topic?</Label>
            <Textarea
              id=\"topic\"
              placeholder=\"e.g., Launching a new product, seasonal sale, company announcement...\"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              rows={3}
              data-testid=\"topic-input\"
            />
          </div>

          <div className=\"grid grid-cols-1 md:grid-cols-3 gap-4\">
            <div className=\"space-y-2\">
              <Label>Platform</Label>
              <Select value={platform} onValueChange={setPlatform}>
                <SelectTrigger data-testid=\"platform-select\">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value=\"social_media\">Social Media</SelectItem>
                  <SelectItem value=\"blog\">Blog Post</SelectItem>
                  <SelectItem value=\"email\">Email</SelectItem>
                  <SelectItem value=\"ad_copy\">Ad Copy</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className=\"space-y-2\">
              <Label>Tone</Label>
              <Select value={tone} onValueChange={setTone}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value=\"professional\">Professional</SelectItem>
                  <SelectItem value=\"casual\">Casual</SelectItem>
                  <SelectItem value=\"friendly\">Friendly</SelectItem>
                  <SelectItem value=\"persuasive\">Persuasive</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className=\"space-y-2\">
              <Label>Length</Label>
              <Select value={length} onValueChange={setLength}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value=\"short\">Short</SelectItem>
                  <SelectItem value=\"medium\">Medium</SelectItem>
                  <SelectItem value=\"long\">Long</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button
            onClick={handleGenerate}
            disabled={loading}
            className=\"w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700\"
            data-testid=\"generate-button\"
          >
            {loading ? 'Generating...' : 'Generate Content'}
          </Button>
        </CardContent>
      </Card>

      {generatedContent && (
        <Card data-testid=\"generated-content\">
          <CardHeader>
            <CardTitle className=\"flex items-center justify-between\">
              <span>Generated Content</span>
              <Button
                variant=\"outline\"
                size=\"sm\"
                onClick={handleCopy}
                data-testid=\"copy-button\"
              >
                {copied ? <Check className=\"w-4 h-4 mr-2\" /> : <Copy className=\"w-4 h-4 mr-2\" />}
                {copied ? 'Copied!' : 'Copy'}
              </Button>
            </CardTitle>
            <CardDescription>
              Platform: {generatedContent.platform.replace('_', ' ')}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className=\"bg-gray-50 rounded-lg p-4 whitespace-pre-wrap\">
              {generatedContent.content}
            </div>
            {generatedContent.hashtags && (
              <div className=\"mt-4\">
                <Label className=\"text-sm text-gray-600\">Suggested Hashtags:</Label>
                <div className=\"flex flex-wrap gap-2 mt-2\">
                  {generatedContent.hashtags.map((tag, idx) => (
                    <span key={idx} className=\"bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm\">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default AutoPublisher;