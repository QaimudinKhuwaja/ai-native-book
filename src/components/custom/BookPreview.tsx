import React from 'react';

function BookPreview() {
  const chapters = [
    { id: 1, title: 'Introduction to AI-Native Development', description: 'Understand the core concepts.' },
    { id: 2, title: 'Foundations of AI-Native Systems', description: 'Explore key architectural patterns.' },
    { id: 3, title: 'Implementing AI-Native Workflows', description: 'Practical approaches and tools.' },
    { id: 4, title: 'Operationalizing AI-Native Solutions', description: 'Deployment and monitoring.' },
    { id: 5, title: 'The Future of AI-Native', description: 'Emerging trends and impact.' },
  ];

  return (
    <div className="container my-8">
      <h2 className="text-3xl font-bold text-center mb-6">Explore the Book</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {chapters.map((chapter) => (
          <div key={chapter.id} className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold mb-2">{chapter.title}</h3>
            <p className="text-gray-600 dark:text-gray-300">{chapter.description}</p>
            <a href={`/docs/${chapter.id}-chapter-slug`} className="mt-4 inline-block text-blue-500 hover:underline">
              Read Chapter {chapter.id}
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default BookPreview;
