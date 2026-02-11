import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Label } from '../ui/label';
import { Input } from '../ui/input';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '../ui/dialog';
import { toast } from 'sonner';
import { DollarSign, Plus, TrendingUp, Eye } from 'lucide-react';

const ROICalculator = () => {
  const { token, API } = useAuth();
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const [roiData, setRoiData] = useState(null);
  const [showCreate, setShowCreate] = useState(false);
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    platform: '',
    spend: '',
    revenue: '',
    impressions: '',
    clicks: '',
    conversions: ''
  });

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    try {
      const response = await axios.get(`${API}/marketing/campaigns`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCampaigns(response.data.campaigns);
    } catch (error) {
      console.error('Failed to fetch campaigns:', error);
    }
  };

  const handleCreateCampaign = async () => {
    if (!newCampaign.name || !newCampaign.platform || !newCampaign.spend) {
      toast.error('Please fill required fields (name, platform, spend)');
      return;
    }

    setLoading(true);
    try {
      await axios.post(
        `${API}/marketing/campaigns`,
        {
          ...newCampaign,
          spend: parseFloat(newCampaign.spend),
          revenue: parseFloat(newCampaign.revenue) || 0,
          impressions: parseInt(newCampaign.impressions) || 0,
          clicks: parseInt(newCampaign.clicks) || 0,
          conversions: parseInt(newCampaign.conversions) || 0,
          start_date: new Date().toISOString()
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Campaign created!');
      setShowCreate(false);
      setNewCampaign({ name: '', platform: '', spend: '', revenue: '', impressions: '', clicks: '', conversions: '' });
      fetchCampaigns();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create campaign');
    } finally {
      setLoading(false);
    }
  };

  const handleCalculateROI = async (campaignId) => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${API}/marketing/campaigns/${campaignId}/roi`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setRoiData(response.data);
      setSelectedCampaign(campaigns.find(c => c.id === campaignId));
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to calculate ROI');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6" data-testid="roi-calculator">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="w-6 h-6 text-purple-600" />
                Marketing ROI Tracker
              </CardTitle>
              <CardDescription>
                Track campaign performance and calculate ROI automatically
              </CardDescription>
            </div>
            <Dialog open={showCreate} onOpenChange={setShowCreate}>
              <DialogTrigger asChild>
                <Button className="bg-gradient-to-r from-purple-600 to-pink-600">
                  <Plus className="w-4 h-4 mr-2" />
                  New Campaign
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Create New Campaign</DialogTitle>
                  <DialogDescription>Add a new marketing campaign to track</DialogDescription>
                </DialogHeader>
                <div className="space-y-4 mt-4">
                  <div className="space-y-2">
                    <Label>Campaign Name *</Label>
                    <Input
                      placeholder="Summer Sale 2025"
                      value={newCampaign.name}
                      onChange={(e) => setNewCampaign({ ...newCampaign, name: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Platform *</Label>
                    <Input
                      placeholder="Facebook, Google, Instagram"
                      value={newCampaign.platform}
                      onChange={(e) => setNewCampaign({ ...newCampaign, platform: e.target.value })}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Spend ($) *</Label>
                      <Input
                        type="number"
                        placeholder="1000"
                        value={newCampaign.spend}
                        onChange={(e) => setNewCampaign({ ...newCampaign, spend: e.target.value })}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Revenue ($)</Label>
                      <Input
                        type="number"
                        placeholder="5000"
                        value={newCampaign.revenue}
                        onChange={(e) => setNewCampaign({ ...newCampaign, revenue: e.target.value })}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label>Impressions</Label>
                      <Input
                        type="number"
                        placeholder="10000"
                        value={newCampaign.impressions}
                        onChange={(e) => setNewCampaign({ ...newCampaign, impressions: e.target.value })}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Clicks</Label>
                      <Input
                        type="number"
                        placeholder="500"
                        value={newCampaign.clicks}
                        onChange={(e) => setNewCampaign({ ...newCampaign, clicks: e.target.value })}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Conversions</Label>
                      <Input
                        type="number"
                        placeholder="50"
                        value={newCampaign.conversions}
                        onChange={(e) => setNewCampaign({ ...newCampaign, conversions: e.target.value })}
                      />
                    </div>
                  </div>
                  <Button
                    onClick={handleCreateCampaign}
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? 'Creating...' : 'Create Campaign'}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </CardHeader>
        <CardContent>
          {campaigns.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <DollarSign className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>No campaigns yet. Create your first campaign to start tracking ROI!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {campaigns.map((campaign) => (
                <Card key={campaign.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold">{campaign.name}</h3>
                        <p className="text-sm text-gray-600">
                          {campaign.platform} • ${campaign.spend} spent
                        </p>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleCalculateROI(campaign.id)}
                        disabled={loading}
                      >
                        <Eye className="w-4 h-4 mr-2" />
                        View ROI
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {roiData && selectedCampaign && (
        <Card data-testid="roi-results">
          <CardHeader>
            <CardTitle>{selectedCampaign.name} - ROI Analysis</CardTitle>
            <CardDescription>Platform: {selectedCampaign.platform}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <Card>
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">ROI</p>
                  <p className={`text-2xl font-bold ${roiData.roi >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {roiData.roi}%
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">ROAS</p>
                  <p className="text-2xl font-bold">{roiData.roas}x</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Profit</p>
                  <p className={`text-2xl font-bold ${roiData.profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    ${roiData.profit}
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Cost Per Click</p>
                  <p className="text-2xl font-bold">${roiData.cpc}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Cost Per Acquisition</p>
                  <p className="text-2xl font-bold">${roiData.cpa}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Conversion Rate</p>
                  <p className="text-2xl font-bold">{roiData.conversion_rate}%</p>
                </CardContent>
              </Card>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ROICalculator;