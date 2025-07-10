import React, { useState, useEffect } from 'react';

interface AIReport {
  summary: string;
  recommendations: string[];
  metrics: {
    sales: number;
    staff: number;
    inventory: number;
    customer: number;
  };
}

const AIAnalytics: React.FC = () => {
  const [report, setReport] = useState<AIReport | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    generateAIReport();
  }, []);

  const generateAIReport = async () => {
    setLoading(true);
    // TODO: 실제 AI 분석 API 호출
    setTimeout(() => {
      setReport({
        summary: "이번 주 매장 운영 분석 결과, 인력 배치 최적화와 재고 관리 개선이 필요합니다.",
        recommendations: [
          "금요일 저녁 시간대 인력 2명 추가 배치 권장",
          "A상품 재고 발주량 20% 증가 필요",
          "고객 피드백 분석 결과: 서비스 응답 시간 개선 필요",
          "이번 달 마케팅 예산 효율성 15% 향상"
        ],
        metrics: {
          sales: 12500000,
          staff: 8,
          inventory: 85,
          customer: 92
        }
      });
      setLoading(false);
    }, 2000);
  };

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!report) return null;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6">
      <div className="flex items-center space-x-3 mb-6">
        <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-purple-600 rounded-xl flex items-center justify-center">
          <span className="text-2xl">🤖</span>
        </div>
        <div>
          <h3 className="text-xl font-bold text-gray-900 dark:text-white">AI 운영 분석</h3>
          <p className="text-sm text-gray-500">실시간 매장 최적화 추천</p>
        </div>
      </div>

      <div className="space-y-6">
        {/* 요약 */}
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
          <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">분석 요약</h4>
          <p className="text-sm text-blue-800 dark:text-blue-200">{report.summary}</p>
        </div>

        {/* 추천사항 */}
        <div>
          <h4 className="font-medium text-gray-900 dark:text-white mb-3">개선 추천사항</h4>
          <div className="space-y-2">
            {report.recommendations.map((rec, index) => (
              <div key={index} className="flex items-start space-x-2 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <span className="text-green-500 mt-0.5">✓</span>
                <span className="text-sm text-gray-700 dark:text-gray-300">{rec}</span>
              </div>
            ))}
          </div>
        </div>

        {/* 지표 */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{report.metrics.sales.toLocaleString()}</div>
            <div className="text-xs text-green-600">월 매출 (원)</div>
          </div>
          <div className="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">{report.metrics.staff}</div>
            <div className="text-xs text-blue-600">최적 인력</div>
          </div>
          <div className="text-center p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">{report.metrics.inventory}%</div>
            <div className="text-xs text-yellow-600">재고 효율성</div>
          </div>
          <div className="text-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
            <div className="text-2xl font-bold text-purple-600">{report.metrics.customer}%</div>
            <div className="text-xs text-purple-600">고객 만족도</div>
          </div>
        </div>

        <button
          onClick={generateAIReport}
          className="w-full px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-300"
        >
          새로운 분석 생성
        </button>
      </div>
    </div>
  );
};

export default AIAnalytics; 