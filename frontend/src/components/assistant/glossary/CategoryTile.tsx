import BackgroundPanelWithHero from "../shared/BackgroundPanelWithHero";
import { GlossaryCategory } from "@/types/assistant";

const CategoryTile = ({ category }: { category: GlossaryCategory }) => {
  return (
    <BackgroundPanelWithHero
      className="max-w-[400px] w-[300px] max-sm:w-[250px]"
      title={category.name}
      heroImg={category.imageSrc ?? "/assets/images/glossary/hero/default.svg"}
      url={`/assistant/glossary/details/cat/${category.id}`}
    >
      {category.description}
    </BackgroundPanelWithHero>
  );
};

export default CategoryTile;
