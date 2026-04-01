"use client";

import { useState, useRef } from "react";

const MODELS = [
  { id: "gemini-3-pro-image-preview", name: "Gemini 3 Pro Image", tier: "최고 품질" },
  { id: "gemini-3.1-flash-image-preview", name: "Gemini 3.1 Flash Image", tier: "고품질 + 빠름" },
  { id: "gemini-2.5-flash-image", name: "Gemini 2.5 Flash Image", tier: "안정적" },
  { id: "nano-banana-pro-preview", name: "Nano Banana Pro", tier: "나노바나나 🍌" },
  { id: "gemini-2.0-flash", name: "Gemini 2.0 Flash", tier: "경량" },
];

export default function Home() {
  const [apiKey, setApiKey] = useState(
    process.env.NEXT_PUBLIC_GEMINI_API_KEY || ""
  );
  const [model, setModel] = useState(MODELS[0].id);
  const [prompt, setPrompt] = useState("");
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [refImages, setRefImages] = useState<{ base64: string; mimeType: string; preview: string }[]>([]);
  const abortRef = useRef<AbortController | null>(null);

  const fileToBase64 = (file: File): Promise<{ base64: string; mimeType: string; preview: string }> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = reader.result as string;
        const base64 = dataUrl.split(",")[1];
        resolve({ base64, mimeType: file.type, preview: dataUrl });
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const handleFiles = async (files: FileList | File[]) => {
    const imageFiles = Array.from(files).filter((f) => f.type.startsWith("image/"));
    if (imageFiles.length === 0) return;
    const results = await Promise.all(imageFiles.map(fileToBase64));
    setRefImages((prev) => [...prev, ...results]);
  };

  const handlePaste = async (e: React.ClipboardEvent) => {
    const items = e.clipboardData?.items;
    if (!items) return;
    const imageFiles: File[] = [];
    for (const item of Array.from(items)) {
      if (item.type.startsWith("image/")) {
        const file = item.getAsFile();
        if (file) imageFiles.push(file);
      }
    }
    if (imageFiles.length > 0) {
      e.preventDefault();
      await handleFiles(imageFiles);
    }
  };

  const removeRefImage = (index: number) => {
    setRefImages((prev) => prev.filter((_, i) => i !== index));
  };

  const generateImage = async () => {
    if (!apiKey.trim()) {
      setError("API Key를 입력해주세요.");
      return;
    }
    if (!prompt.trim()) {
      setError("프롬프트를 입력해주세요.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      abortRef.current = new AbortController();

      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          signal: abortRef.current.signal,
          body: JSON.stringify({
            contents: [
              {
                parts: [
                  ...refImages.map((img) => ({
                    inlineData: { mimeType: img.mimeType, data: img.base64 },
                  })),
                  { text: prompt },
                ],
              },
            ],
            generationConfig: {
              responseModalities: ["TEXT", "IMAGE"],
            },
          }),
        }
      );

      if (!response.ok) {
        const errData = await response.json().catch(() => null);
        throw new Error(
          errData?.error?.message || `API 오류: ${response.status}`
        );
      }

      const data = await response.json();
      const parts = data.candidates?.[0]?.content?.parts || [];
      const newImages: string[] = [];

      for (const part of parts) {
        if (part.inlineData) {
          const base64 = part.inlineData.data;
          const mimeType = part.inlineData.mimeType || "image/png";
          newImages.push(`data:${mimeType};base64,${base64}`);
        }
      }

      if (newImages.length === 0) {
        const textPart = parts.find((p: { text?: string }) => p.text);
        throw new Error(
          textPart?.text || "이미지가 생성되지 않았습니다. 프롬프트를 수정해보세요."
        );
      }

      setImages((prev) => [...newImages, ...prev]);

      // 자동 다운로드
      newImages.forEach((img, i) => {
        const link = document.createElement("a");
        link.href = img;
        link.download = `gemini-${Date.now()}-${i}.png`;
        link.click();
      });
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") return;
      setError(err instanceof Error ? err.message : "알 수 없는 오류");
    } finally {
      setLoading(false);
    }
  };

  const downloadImage = (dataUrl: string, index: number) => {
    const link = document.createElement("a");
    link.href = dataUrl;
    link.download = `gemini-image-${Date.now()}-${index}.png`;
    link.click();
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4">
        <h1 className="text-2xl font-bold tracking-tight">
          ✨ Gemini Image Generator
        </h1>
        <p className="text-sm text-gray-400 mt-1">
          Gemini API로 이미지를 생성하세요
        </p>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8 space-y-6">
        {/* API Key */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">API Key</label>
          <div className="flex gap-2">
            <input
              type={showKey ? "text" : "password"}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Gemini API Key를 입력하세요"
              className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 placeholder-gray-500"
            />
            <button
              onClick={() => setShowKey(!showKey)}
              className="px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-lg text-sm hover:bg-gray-700 transition-colors shrink-0"
            >
              {showKey ? "숨기기" : "보기"}
            </button>
          </div>
        </div>

        {/* Model Select */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">모델 선택</label>
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 appearance-none cursor-pointer"
          >
            {MODELS.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name} — {m.tier}
              </option>
            ))}
          </select>
        </div>

        {/* Prompt */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">프롬프트</label>
          {refImages.length > 0 && (
            <div className="flex gap-2 flex-wrap">
              {refImages.map((img, i) => (
                <div key={i} className="relative group w-16 h-16">
                  <img
                    src={img.preview}
                    alt={`ref-${i}`}
                    className="w-16 h-16 object-cover rounded-lg border border-gray-700"
                  />
                  <button
                    onClick={() => removeRefImage(i)}
                    className="absolute -top-2 -right-2 w-5 h-5 bg-red-600 rounded-full text-xs flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    x
                  </button>
                </div>
              ))}
            </div>
          )}
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onPaste={handlePaste}
            placeholder="생성하고 싶은 이미지를 설명하세요... (Ctrl+V로 이미지 붙여넣기 가능)&#10;예: 이 사진을 참고해서 비슷한 스타일로 만들어줘"
            rows={4}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 placeholder-gray-500 resize-none"
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                generateImage();
              }
            }}
          />
          <p className="text-xs text-gray-500">Ctrl + Enter로 생성 · Ctrl + V로 이미지 붙여넣기</p>
        </div>

        {/* Generate Button */}
        <button
          onClick={generateImage}
          disabled={loading}
          className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 disabled:cursor-not-allowed rounded-lg font-medium transition-colors text-sm"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg
                className="animate-spin h-4 w-4"
                viewBox="0 0 24 24"
                fill="none"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              생성 중...
            </span>
          ) : (
            "이미지 생성"
          )}
        </button>

        {/* Error */}
        {error && (
          <div className="bg-red-900/30 border border-red-800 rounded-lg px-4 py-3 text-sm text-red-300">
            {error}
          </div>
        )}

        {/* Images */}
        {images.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">
                생성된 이미지 ({images.length})
              </h2>
              <button
                onClick={() => setImages([])}
                className="text-sm text-gray-400 hover:text-red-400 transition-colors"
              >
                전체 삭제
              </button>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {images.map((img, i) => (
                <div
                  key={i}
                  className="group relative bg-gray-900 border border-gray-800 rounded-xl overflow-hidden"
                >
                  <img
                    src={img}
                    alt={`Generated ${i + 1}`}
                    className="w-full h-auto"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <button
                      onClick={() => downloadImage(img, i)}
                      className="px-4 py-2 bg-white text-black rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors"
                    >
                      다운로드
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
