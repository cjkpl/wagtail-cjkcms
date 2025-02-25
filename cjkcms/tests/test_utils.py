import unittest
from cjkcms.blocks import (
    GridBlock,
    HeroBlock,
    AccordionBlock,
    CardBlock,
    ButtonBlock,
    CardGridBlock,
    # replace_contentblocks,
)


class TestReplaceContentBlocks(unittest.TestCase):
    def setUp(self):
        self.old_content_blocks = [
            ("accordion", AccordionBlock()),
            ("card", CardBlock()),
        ]
        self.flat_layout_blocks = [
            ("row", GridBlock(self.old_content_blocks)),
            (
                "cardgrid",
                CardGridBlock(
                    [
                        ("card", CardBlock()),
                    ]
                ),
            ),
        ]
        self.full_layout_blocks = [
            ("hero", HeroBlock(self.flat_layout_blocks)),
            *self.flat_layout_blocks,
        ]
        self.new_content_blocks = [
            *self.old_content_blocks,
            ("button", ButtonBlock()),
        ]

    def test_replace_contentblocks(self):
        pass
        # updated_full_layout_blocks = replace_contentblocks(
        #     self.flat_layout_blocks, self.full_layout_blocks, self.new_content_blocks
        # )

        # Check if the top-level "row" block is replaced
        # self.assertIsInstance(updated_full_layout_blocks[0][1], HeroBlock)
        # self.assertEqual(
        #     updated_full_layout_blocks[0][1]
        #     .content_streamblocks[0][1]
        #     .contet_streamblocks,
        #     self.new_content_blocks,
        # )

    #     # Check if the "hero" block is updated correctly
    #     self.assertIsInstance(updated_full_layout_blocks[0][1], HeroBlock)
    #     self.assertEqual(
    #         updated_full_layout_blocks[0][1].streamblock[0][1].streamblock,
    #         self.new_content_blocks,
    #     )

    # def test_no_replacement_for_non_matching_blocks(self):
    #     non_matching_structure = [
    #         ("cardgrid", CardGridBlock),
    #         ("button", ButtonBlock),
    #     ]
    #     updated_full_layout_blocks = replace_contentblocks(
    #         non_matching_structure, self.full_layout_blocks, self.new_content_blocks
    #     )

    #     # Check if the structure remains unchanged
    #     self.assertEqual(updated_full_layout_blocks[1], non_matching_structure)

    # def test_empty_structure(self):
    #     empty_structure = []
    #     updated_full_layout_blocks = replace_contentblocks(
    #         empty_structure, self.full_layout_blocks, self.new_content_blocks
    #     )

    #     # Check if the structure remains unchanged
    #     self.assertEqual(updated_full_layout_blocks[1], empty_structure)
