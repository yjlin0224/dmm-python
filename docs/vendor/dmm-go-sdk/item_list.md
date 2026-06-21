# Item List

<!-- markdownlint-disable MD010 -->

<https://github.com/dmmlabo/dmm-go-sdk/blob/f67870f8/api/product.go#L17-L148>

```go
type ProductService struct {
	ApiID       string `mapstructure:"api_id"`
	AffiliateID string `mapstructure:"affiliate_id"`
	Site        string `mapstructure:"site"`
	Service     string `mapstructure:"service"`
	Floor       string `mapstructure:"floor"`
	Length      int64  `mapstructure:"hits"`
	Offset      int64  `mapstructure:"offset"`
	Sort        string `mapstructure:"sort"`
	Keyword     string `mapstructure:"keyword"`
	ContentID   string `mapstructure:"cid"`
	Article     string `mapstructure:"article"`
	ArticleID   string `mapstructure:"article_id"`
	GteDate     string `mapstructure:"gte_date"`
	LteDate     string `mapstructure:"lte_date"`
	Stock       string `mapstructure:"mono_stock"`
}

type ProductRawResponse struct {
	Request ProductService  `mapstructure:"request"`
	Result  ProductResponse `mapstructure:"result"`
}

type ProductResponse struct {
	ResultCount   int64  `mapstructure:"result_count"`
	TotalCount    int64  `mapstructure:"total_count"`
	FirstPosition int64  `mapstructure:"first_position"`
	Items         []Item `mapstructure:"items"`
}

type Item struct {
	AffiliateURL       string             `mapstructure:"affiliateURL"`
	AffiliateURLMobile string             `mapstructure:"affiliateURLsp"`
	CategoryName       string             `mapstructure:"category_name"`
	Comment            string             `mapstructure:"comment"`
	ContentID          string             `mapstructure:"content_id"`
	Date               string             `mapstructure:"date"`
	FloorName          string             `mapstructure:"floor_name"`
	FloorCode          string             `mapstructure:"floor_code"`
	ISBN               string             `mapstructure:"isbn"`
	JANCode            string             `mapstructure:"jancode"`
	ProductCode        string             `mapstructure:"maker_product"`
	ProductID          string             `mapstructure:"product_id"`
	ServiceName        string             `mapstructure:"service_name"`
	ServiceCode        string             `mapstructure:"service_code"`
	Stock              string             `mapstructure:"stock"`
	Title              string             `mapstructure:"title"`
	URL                string             `mapstructure:"URL"`
	URLMobile          string             `mapstructure:"URLsp"`
	Volume             string             `mapstructure:"volume"`
	ImageURL           ImageURLList       `mapstructure:"imageURL"`
	SampleImageURL     SampleImageURLList `mapstructure:"sampleImageURL"`
	SampleMovieURL     SampleMovieURLList `mapstructure:"sampleMovieURL"`
	Review             ReviewInformation  `mapstructure:"review"`
	PriceInformation   PriceInformation   `mapstructure:"prices"`
	ItemInformation    ItemInformation    `mapstructure:"iteminfo"`
	BandaiInformation  BandaiInformation  `mapstructure:"bandaiinfo"`
	CdInformation      CdInformation      `mapstructure:"cdinfo"`
}

type ImageURLList struct {
	List  string `mapstructure:"list"`
	Small string `mapstructure:"small"`
	Large string `mapstructure:"large"`
}

type SampleImageURLList struct {
	SampleS SmallSampleList `mapstructure:"sample_s"`
}

type SmallSampleList struct {
	Image []string `mapstructure:"image"`
}

type SampleMovieURLList struct {
	Size476_306 string `mapstructure:"size_476_306"`
	Size560_360 string `mapstructure:"size_560_360"`
	Size644_414 string `mapstructure:"size_644_414"`
	Size720_480 string `mapstructure:"size_720_480"`
	PCFlag      bool   `mapstructure:"pc_flag"`
	SPFlag      bool   `mapstructure:"sp_flag"`
}

type PriceInformation struct {
	Price         string           `mapstructure:"price"`
	PriceAll      string           `mapstructure:"price_all"`
	RetailPrice   string           `mapstructure:"list_price"`
	Distributions DistributionList `mapstructure:"deliveries"`
}

type DistributionList struct {
	Distribution []Distribution `mapstructure:"delivery"`
}

type Distribution struct {
	Type  string `mapstructure:"type"`
	Price string `mapstructure:"price"`
}

type ItemInformation struct {
	Maker     []ItemComponent `mapstructure:"maker"`
	Label     []ItemComponent `mapstructure:"label"`
	Series    []ItemComponent `mapstructure:"series"`
	Keywords  []ItemComponent `mapstructure:"keyword"`
	Genres    []ItemComponent `mapstructure:"genre"`
	Actors    []ItemComponent `mapstructure:"actor"`
	Artists   []ItemComponent `mapstructure:"artist"`
	Authors   []ItemComponent `mapstructure:"author"`
	Directors []ItemComponent `mapstructure:"director"`
	Fighters  []ItemComponent `mapstructure:"fighter"`
	Colors    []ItemComponent `mapstructure:"color"`
	Sizes     []ItemComponent `mapstructure:"size"`
	Actresses []ItemComponent `mapstructure:"actress"`
}

type ItemComponent struct {
	ID   string `mapstructure:"id"`
	Name string `mapstructure:"name"`
}

type BandaiInformation struct {
	TitleCode string `mapstructure:"titlecode"`
}

type CdInformation struct {
	Kind string `mapstructure:"kind"`
}

type ReviewInformation struct {
	Count   int64   `mapstructure:"count"`
	Average float64 `mapstructure:"average"`
}
```
