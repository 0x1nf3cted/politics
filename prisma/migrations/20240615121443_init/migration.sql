-- CreateTable
CREATE TABLE "Newspaper" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "orientation" TEXT,
    "url" TEXT,

    CONSTRAINT "Newspaper_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Article" (
    "id" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "author" TEXT,
    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "image_url" TEXT NOT NULL,
    "general_category" TEXT NOT NULL,
    "category" TEXT NOT NULL,
    "date" TEXT NOT NULL,
    "newspaperId" TEXT NOT NULL,
    "collectionId" TEXT,

    CONSTRAINT "Article_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Collection" (
    "id" TEXT NOT NULL,
    "date" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "category" TEXT NOT NULL,

    CONSTRAINT "Collection_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Rssfeed" (
    "id" TEXT NOT NULL,
    "general_category" TEXT NOT NULL,
    "specific_category" TEXT NOT NULL,
    "rss_link" TEXT NOT NULL,
    "newspaperId" TEXT NOT NULL,

    CONSTRAINT "Rssfeed_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Newspaper_id_key" ON "Newspaper"("id");

-- CreateIndex
CREATE UNIQUE INDEX "Article_id_key" ON "Article"("id");

-- CreateIndex
CREATE UNIQUE INDEX "Collection_id_key" ON "Collection"("id");

-- CreateIndex
CREATE UNIQUE INDEX "Rssfeed_id_key" ON "Rssfeed"("id");

-- AddForeignKey
ALTER TABLE "Article" ADD CONSTRAINT "Article_newspaperId_fkey" FOREIGN KEY ("newspaperId") REFERENCES "Newspaper"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Article" ADD CONSTRAINT "Article_collectionId_fkey" FOREIGN KEY ("collectionId") REFERENCES "Collection"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Rssfeed" ADD CONSTRAINT "Rssfeed_newspaperId_fkey" FOREIGN KEY ("newspaperId") REFERENCES "Newspaper"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
