# Actress Search

<!-- markdownlint-disable MD010 -->

<https://github.com/dmmlabo/dmm-go-sdk/blob/f67870f8/api/actress.go#L18-L94>

```go
type ActressService struct {
	ApiID       string `mapstructure:"api_id"`
	AffiliateID string `mapstructure:"affiliate_id"`
	Length      int64  `mapstructure:"hits"`
	Offset      int64  `mapstructure:"offset"`
	Sort        string `mapstructure:"sort"`
	Initial     string `mapstructure:"initial"`
	ActressID   string `mapstructure:"actress_id"`
	Keyword     string `mapstructure:"keyword"`
	Bust        string `mapstructure:"bust"`
	GteBust     string `mapstructure:"gte_bust"`
	LteBust     string `mapstructure:"lte_bust"`
	Waist       string `mapstructure:"waist"`
	GteWaist    string `mapstructure:"gte_waist"`
	LteWaist    string `mapstructure:"lte_waist"`
	Hip         string `mapstructure:"hip"`
	GteHip      string `mapstructure:"gte_hip"`
	LteHip      string `mapstructure:"lte_hip"`
	Height      string `mapstructure:"height"`
	GteHeight   string `mapstructure:"gte_height"`
	LteHeight   string `mapstructure:"lte_height"`
	Birthday    string `mapstructure:"birthday"`
	GteBirthday string `mapstructure:"gte_birthday"`
	LteBirthday string `mapstructure:"lte_birthday"`
}

type ActressRawResponse struct {
	Request ActressService  `mapstructure:"request"`
	Result  ActressResponse `mapstructure:"result"`
}

type ActressResponse struct {
	ResultCount   int64     `mapstructure:"result_count"`
	TotalCount    int64     `mapstructure:"total_count"`
	FirstPosition int64     `mapstructure:"first_position"`
	Actresses     []Actress `mapstructure:"actress"`
}

type Actress struct {
	ID          string             `mapstructure:"id"`
	Name        string             `mapstructure:"name"`
	Ruby        string             `mapstructure:"ruby"`
	Bust        string             `mapstructure:"bust"`
	GteBust     string             `mapstructure:"gte_bust"`
	LteBust     string             `mapstructure:"lte_bust"`
	Cup         string             `mapstructure:"cup"`
	Waist       string             `mapstructure:"waist"`
	GteWaist    string             `mapstructure:"gte_waist"`
	LteWaist    string             `mapstructure:"lte_waist"`
	Hip         string             `mapstructure:"hip"`
	GteHip      string             `mapstructure:"gte_hip"`
	LteHip      string             `mapstructure:"lte_hip"`
	Height      string             `mapstructure:"height"`
	GteHeight   string             `mapstructure:"gte_height"`
	LteHeight   string             `mapstructure:"lte_height"`
	Birthday    string             `mapstructure:"birthday"`
	GteBirthday string             `mapstructure:"gte_birthday"`
	LteBirthday string             `mapstructure:"lte_birthday"`
	BloodType   string             `mapstructure:"blood_type"`
	Hobby       string             `mapstructure:"hobby"`
	Prefectures string             `mapstructure:"prefectures"`
	ImageURL    ActressImageList   `mapstructure:"imageURL"`
	ListURL     ActressProductList `mapstructure:"listURL"`
}

type ActressImageList struct {
	Small string `mapstructure:"small"`
	Large string `mapstructure:"large"`
}

type ActressProductList struct {
	Digital string `mapstructure:"digital"`
	Mono    string `mapstructure:"mono"`
	Monthly string `mapstructure:"monthly"`
	Ppm     string `mapstructure:"ppm"`
	Rental  string `mapstructure:"rental"`
}
```
